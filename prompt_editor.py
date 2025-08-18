#!/usr/bin/env python3
"""
Prompt编辑工具 - 方便编辑和管理Prompt配置
"""

import os
import sys
import yaml
from typing import Dict, Any

def load_prompts_config() -> Dict[str, Any]:
    """加载Prompt配置"""
    config_path = os.path.join("config", "prompts_config.yaml")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

def save_prompts_config(config: Dict[str, Any]):
    """保存Prompt配置"""
    config_path = os.path.join("config", "prompts_config.yaml")
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, indent=2)

def display_prompts(config: Dict[str, Any]):
    """显示所有Prompt"""
    print("📝 当前Prompt配置:")
    print("=" * 50)
    
    for prompt_name, prompt_data in config.items():
        print(f"\n🎭 {prompt_name}:")
        print(f"   名称: {prompt_data.get('name', 'N/A')}")
        print(f"   系统提示词长度: {len(prompt_data.get('system_prompt', ''))} 字符")
        print(f"   示例数量: {len(prompt_data.get('examples', []))}")
        
        # 显示系统提示词预览
        system_prompt = prompt_data.get('system_prompt', '')
        if system_prompt:
            preview = system_prompt[:100] + "..." if len(system_prompt) > 100 else system_prompt
            print(f"   提示词预览: {preview}")

def add_new_prompt():
    """添加新的Prompt"""
    print("\n➕ 添加新Prompt")
    print("-" * 30)
    
    prompt_name = input("请输入Prompt名称 (例如: little_prince_v2): ").strip()
    if not prompt_name:
        print("❌ Prompt名称不能为空")
        return
    
    name = input("请输入显示名称: ").strip() or prompt_name
    
    print("\n📝 请输入系统提示词 (输入 'END' 结束):")
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    
    system_prompt = '\n'.join(lines)
    
    # 添加示例
    examples = []
    print("\n💬 是否添加示例对话? (y/n): ", end='')
    if input().lower().startswith('y'):
        while True:
            print(f"\n示例 {len(examples) + 1}:")
            user_input = input("用户输入 (留空结束): ").strip()
            if not user_input:
                break
            
            assistant_input = input("小王子回复: ").strip()
            if assistant_input:
                examples.append({
                    "user": user_input,
                    "assistant": assistant_input
                })
    
    # 创建新Prompt
    new_prompt = {
        "name": name,
        "system_prompt": system_prompt,
        "examples": examples
    }
    
    return prompt_name, new_prompt

def edit_prompt(config: Dict[str, Any]):
    """编辑现有Prompt"""
    print("\n✏️ 编辑Prompt")
    print("-" * 30)
    
    # 显示可用的Prompt
    prompt_names = list(config.keys())
    for i, name in enumerate(prompt_names, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input(f"\n请选择要编辑的Prompt (1-{len(prompt_names)}): ")) - 1
        if 0 <= choice < len(prompt_names):
            prompt_name = prompt_names[choice]
            prompt_data = config[prompt_name]
            
            print(f"\n当前编辑: {prompt_name}")
            print("1. 修改系统提示词")
            print("2. 修改示例对话")
            print("3. 修改显示名称")
            
            sub_choice = input("请选择操作 (1-3): ").strip()
            
            if sub_choice == "1":
                print("\n📝 请输入新的系统提示词 (输入 'END' 结束):")
                lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    lines.append(line)
                prompt_data["system_prompt"] = '\n'.join(lines)
                
            elif sub_choice == "2":
                print("\n💬 重新输入示例对话 (输入 'END' 结束):")
                examples = []
                while True:
                    user_input = input("用户输入 (留空结束): ").strip()
                    if not user_input:
                        break
                    
                    assistant_input = input("小王子回复: ").strip()
                    if assistant_input:
                        examples.append({
                            "user": user_input,
                            "assistant": assistant_input
                        })
                prompt_data["examples"] = examples
                
            elif sub_choice == "3":
                new_name = input("请输入新的显示名称: ").strip()
                if new_name:
                    prompt_data["name"] = new_name
                    
            print("✅ 修改完成")
        else:
            print("❌ 无效选择")
    except ValueError:
        print("❌ 请输入有效数字")

def delete_prompt(config: Dict[str, Any]):
    """删除Prompt"""
    print("\n🗑️ 删除Prompt")
    print("-" * 30)
    
    prompt_names = list(config.keys())
    for i, name in enumerate(prompt_names, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input(f"\n请选择要删除的Prompt (1-{len(prompt_names)}): ")) - 1
        if 0 <= choice < len(prompt_names):
            prompt_name = prompt_names[choice]
            confirm = input(f"确定要删除 '{prompt_name}' 吗? (y/n): ").strip().lower()
            if confirm.startswith('y'):
                del config[prompt_name]
                print("✅ 删除完成")
            else:
                print("❌ 取消删除")
        else:
            print("❌ 无效选择")
    except ValueError:
        print("❌ 请输入有效数字")

def main():
    """主函数"""
    print("🎭 Prompt编辑工具")
    print("=" * 50)
    
    # 加载配置
    config = load_prompts_config()
    
    while True:
        print("\n📋 请选择操作:")
        print("1. 查看所有Prompt")
        print("2. 添加新Prompt")
        print("3. 编辑Prompt")
        print("4. 删除Prompt")
        print("5. 保存并退出")
        print("6. 退出不保存")
        
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == "1":
            display_prompts(config)
            
        elif choice == "2":
            result = add_new_prompt()
            if result:
                prompt_name, new_prompt = result
                config[prompt_name] = new_prompt
                print("✅ 添加完成")
                
        elif choice == "3":
            if config:
                edit_prompt(config)
            else:
                print("❌ 没有可编辑的Prompt")
                
        elif choice == "4":
            if config:
                delete_prompt(config)
            else:
                print("❌ 没有可删除的Prompt")
                
        elif choice == "5":
            save_prompts_config(config)
            print("✅ 配置已保存")
            break
            
        elif choice == "6":
            print("❌ 未保存更改")
            break
            
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()
