import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { useA2UI } from '../hooks/A2UIContext';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatPanel() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  
  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);
  const { dispatchA2UIEvent } = useA2UI();

  // Connect to WebSocket on mount
  useEffect(() => {
    // Generate a random session ID or use a fixed one for now
    const sessionId = Math.random().toString(36).substring(7);
    // In production, we'd use the current window host, but for dev we hardcode localhost:8000
    wsRef.current = new WebSocket(`ws://localhost:8000/ws/chat`);

    wsRef.current.onopen = () => setIsConnected(true);
    wsRef.current.onclose = () => setIsConnected(false);

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'chunk') {
        setIsTyping(false);
        setMessages((prev) => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];
          if (lastMsg && lastMsg.role === 'assistant') {
            lastMsg.rawContent += data.content;
            lastMsg.displayContent = stripA2UI(lastMsg.rawContent);
          } else {
            newMessages.push({
              role: 'assistant',
              rawContent: data.content,
              displayContent: stripA2UI(data.content),
            });
          }
          return newMessages;
        });
      } else if (data.type === 'a2ui') {
        // Intercept direct A2UI JSON payloads from backend internal broadcast
        dispatchA2UIEvent(data.payload.ui_action, data.payload.data);
      } else if (data.type === 'done') {
        setIsTyping(false);
      } else if (data.type === 'error') {
        console.error("Agent error:", data.content);
        setIsTyping(false);
      }
    };

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // Strip A2UI blocks (legacy support in case LLM outputs it)
  const stripA2UI = (text) => {
    return text.replace(/```a2ui\n[\s\S]*?(```|$)/g, '').trim();
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim() || !isConnected) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      { role: 'user', displayContent: input, rawContent: input },
    ]);
    
    // Send to backend
    wsRef.current.send(JSON.stringify({ prompt: input }));
    setInput('');
    setIsTyping(true);
  };

  return (
    <div className="bg-panel border border-borderRing rounded-lg h-full flex flex-col overflow-hidden">
      <div className="px-4 py-3 border-b border-borderRing font-semibold text-sm flex justify-between items-center shrink-0">
        <span>AI Chat</span>
        <span className="flex items-center gap-2 text-xs text-textSecondary">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-accentUp' : 'bg-accentDown'}`} />
          {isConnected ? 'Connected' : 'Offline'}
        </span>
      </div>

      <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-lg px-4 py-2 text-sm whitespace-pre-wrap ${
              msg.role === 'user' 
                ? 'bg-brand text-white' 
                : 'bg-[#1E2536] text-textPrimary border border-borderRing'
            }`}>
              {msg.role === 'user' ? (
                msg.displayContent
              ) : (
                <div className="markdown-body">
                  <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    components={{
                      table: ({node, ...props}) => <div className="overflow-x-auto my-4"><table className="w-full text-left border-collapse" {...props} /></div>,
                      th: ({node, ...props}) => <th className="border-b border-[#2A3241] py-2 px-3 font-semibold text-textSecondary bg-[#171D2B]" {...props} />,
                      td: ({node, ...props}) => <td className="py-2 px-3 border-b border-[#2A3241] text-textPrimary" {...props} />,
                      p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                      ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-2" {...props} />,
                      ol: ({node, ...props}) => <ol className="list-decimal pl-5 mb-2" {...props} />
                    }}
                  >
                    {msg.displayContent}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-[#1E2536] border border-borderRing rounded-lg px-4 py-2 text-sm text-textSecondary animate-pulse">
              Agent is typing...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="p-3 border-t border-borderRing shrink-0">
        <div className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask VanillaForge..."
            className="w-full bg-[#1E2536] border border-borderRing rounded-md py-2 pl-3 pr-10 text-sm focus:outline-none focus:border-brand transition-colors text-textPrimary placeholder:text-textSecondary"
            disabled={!isConnected}
          />
          <button 
            type="submit" 
            disabled={!isConnected || !input.trim()}
            className="absolute right-2 text-textSecondary hover:text-brand disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
