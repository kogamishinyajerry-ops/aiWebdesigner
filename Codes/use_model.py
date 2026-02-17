import requests
import json
import time
from typing import Dict, Any, Optional

class OllamaClient:
    """Ollama API 客户端，用于与本地运行的 Ollama 服务交互"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """初始化客户端
        
        Args:
            base_url: Ollama 服务的基础 URL
        """
        self.base_url = base_url
        
    def generate(self, 
                model: str, 
                prompt: str, 
                temperature: float = 0.7, 
                max_tokens: int = 1024,
                stream: bool = False) -> Dict[str, Any]:
        """调用模型生成回复
        
        Args:
            model: 要使用的模型名称，如 "deepseek-r1:1.5b"
            prompt: 输入的提示文本
            temperature: 控制生成的随机性，值越低越确定性
            max_tokens: 最大生成的 token 数量
            stream: 是否使用流式响应
            
        Returns:
            模型生成的响应
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        if stream:
            # 处理流式响应
            return self._handle_stream(url, payload)
        else:
            # 处理非流式响应
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    
    def _handle_stream(self, url: str, payload: Dict[str, Any]) -> str:
        """处理流式响应"""
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        full_text = ""
        for line in response.iter_lines():
            if line:
                # 解析 JSON 数据
                data = json.loads(line.decode('utf-8'))
                if 'response' in data:
                    full_text += data['response']
                    # 打印实时生成的文本（可选）
                    print(data['response'], end='', flush=True)
        
        print()  # 换行
        return full_text
    
    def list_models(self) -> Dict[str, Any]:
        """列出所有可用的模型"""
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

# 使用示例
if __name__ == "__main__":
    client = OllamaClient()
    
    # 列出所有可用模型
    print("可用模型列表:")
    models = client.list_models()
    for model in models.get('models', []):
        print(f"- {model['name']}")
    
    # 使用 DeepSeek-R1 模型生成回复
    model_name = "deepseek-r1:1.5b"  # 根据实际情况修改模型名称
    prompt = "请介绍一下量子计算的基本原理"
    
    print(f"\n正在使用 {model_name} 生成回复...")
    start_time = time.time()
    
    # 非流式调用
    response = client.generate(
        model=model_name,
        prompt=prompt,
        temperature=0.7,
        max_tokens=512,
        stream=False  # 设置为 True 可以启用流式输出
    )
    
    end_time = time.time()
    
    # 输出结果
    print(f"生成时间: {end_time - start_time:.2f} 秒")
    print(f"回复: {response.get('response', '')}")