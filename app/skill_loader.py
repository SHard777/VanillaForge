import os
import yaml
import importlib.util
import functools
from typing import List, Callable


def load_dynamic_skills() -> List[Callable]:
    """
    Scans the skills/ directory, reads the YAML metadata from SKILL.md,
    and dynamically loads the corresponding Python functions from scripts/.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = os.path.join(project_root, "skills")

    tools = []

    if not os.path.exists(skills_dir):
        return tools

    for skill_folder in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_folder)
        if not os.path.isdir(skill_path):
            continue

        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            continue

        # Parse YAML frontmatter and extract instructions body
        metadata = {}
        system_instruction = ""
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content.startswith("---"):
                end_idx = content.find("---", 3)
                if end_idx != -1:
                    yaml_content = content[3:end_idx].strip()
                    system_instruction = content[end_idx + 3 :].strip()
                    try:
                        metadata = yaml.safe_load(yaml_content)
                    except yaml.YAMLError:
                        pass
            else:
                system_instruction = content.strip()

        # Now dynamically load scripts inside scripts/ folder
        scripts_dir = os.path.join(skill_path, "scripts")
        if not os.path.exists(scripts_dir):
            continue

        for script_file in os.listdir(scripts_dir):
            if script_file.endswith(".py") and not script_file.startswith("__"):
                module_name = f"{skill_folder}.{script_file[:-3]}"
                file_path = os.path.join(scripts_dir, script_file)

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Extract callable functions that aren't private
                    for attr_name in dir(module):
                        if not attr_name.startswith("_"):
                            attr = getattr(module, attr_name)
                            if callable(attr) and attr.__module__ == module_name:
                                # We optionally inject the YAML description into the docstring
                                if metadata.get("description"):
                                    attr.__doc__ = (
                                        metadata.get("description")
                                        + "\n\n"
                                        + str(attr.__doc__ or "")
                                    )

                                # [ARCHITECTURE NOTE] Automated Progressive Disclosure:
                                # Instead of stuffing massive instructions into the main agent's system prompt (which causes
                                # context memory rot and hallucination), we intercept the tool's return payload.
                                # We only inject the heavy `__agent_instructions__` markdown *after* the specific skill is used.
                                # Wrap the function for automated Progressive Disclosure
                                @functools.wraps(attr)
                                def progressive_disclosure_wrapper(
                                    *args,
                                    _orig_attr=attr,
                                    _sys_inst=system_instruction,
                                    **kwargs,
                                ):
                                    result = _orig_attr(*args, **kwargs)
                                    if isinstance(result, dict) and _sys_inst:
                                        if "__agent_instructions__" not in result:
                                            result["__agent_instructions__"] = (
                                                f"IMPORTANT: Use the following guidelines to format your response to the user:\n\n{_sys_inst}"
                                            )
                                    return result

                                tools.append(progressive_disclosure_wrapper)
    return tools
