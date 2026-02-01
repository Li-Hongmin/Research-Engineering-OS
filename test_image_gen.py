#!/usr/bin/env python3
"""测试Azure图像生成并保存"""

from openai import AzureOpenAI
import base64
from pathlib import Path

client = AzureOpenAI(
    api_key="3e3a7c53784247a6ad61d3f1bed81752",
    api_version="2024-08-01-preview",
    azure_endpoint="https://eastus2.api.cognitive.microsoft.com"
)

print("🎨 测试Azure图像生成\n")

try:
    response = client.images.generate(
        model="gpt-image-1.5",
        prompt="Professional book cover design: 'Research Engineering OS', minimalist style, blue and white colors, clean typography",
        size="1024x1024",
        quality="high",
        n=1
    )
    
    # 获取base64数据
    image_data = response.data[0]
    
    if hasattr(image_data, 'b64_json') and image_data.b64_json:
        print("✅ 收到base64图像数据")
        
        # 解码并保存
        img_bytes = base64.b64decode(image_data.b64_json)
        output_path = Path("test_cover.png")
        
        with open(output_path, 'wb') as f:
            f.write(img_bytes)
        
        print(f"✅ 图像已保存: {output_path}")
        print(f"文件大小: {len(img_bytes) / 1024:.1f} KB")
    
    elif hasattr(image_data, 'url') and image_data.url:
        print(f"✅ 收到URL: {image_data.url}")
    
    else:
        print("❌ 未找到图像数据")
        print(f"Response: {image_data}")

except Exception as e:
    import traceback
    print(f"❌ 失败: {e}")
    traceback.print_exc()

