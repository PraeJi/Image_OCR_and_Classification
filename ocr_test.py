import json, base64, requests
from dotenv import load_dotenv
import os

load_dotenv()

api_endpoint = os.getenv("LLM_API_ENDPOINT")
llm_api_key = os.getenv("LLM_API_KEY")
api_key = f"Bearer {llm_api_key}"

def classify_and_content(image_path):
    # prompt = """Extract ALL text from this document image. 
    #     Maintain the original structure and formatting as much as possible.
    #     Include all visible text, numbers, and special characters.
    #     If the document has a specific format (invoice, resume, etc.), preserve that structure.
    # """
    img_base64 = image_base64(image_path)
    schema_info = content_requests_schema()  # JSON example + constraints

    prompt = f"""
        You are an OCR extraction assistant.

        Task:
        Extract ALL visible text from the image.

        Requirements:
        - Preserve original layout (line breaks, indentation, table structure).
        - Keep every number, symbol, header, footer, watermark, and label.
        - DO NOT summarize or interpret anything — just extract text exactly as seen.
        - Do NOT invent or guess any information. If a field is not present in the image, fill it with "-".

        Output rules:
        1. Return ONLY JSON according to the schema below.
        2. Do not add any extra text, explanation, or commentary.
        3. All fields must be present. If the information cannot be found in the image, use "-".
        4. Do not change the structure or field names.
        5. Strictly follow the example structure.

        Schema Description: {schema_info['description']}

        Example JSON:
        {schema_info['example']}

        Constraints:
        {schema_info['constraints']}
    """
    
    response = requests.post(
        api_endpoint,
        headers={"Authorization": api_key, "Content-Type": "application/json"},
        json={
            "model": "Qwen/Qwen3-VL-235B-A22B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }
            ],
            "temperature": 0.1,
        }
    )

    result = response.json()
    content = result["choices"][0]["message"]["content"]
    # print(content)
    return json.loads(content)
    # return content
    # return result

def content_requests_schema():
    """
    คืนค่า schema สำหรับ embed ใน prompt ของ Qwen
    เป็น JSON ตัวอย่าง + constraints
    """
    schema = {
        "description": "โปรดตอบกลับเป็น JSON ตาม schema นี้เท่านั้น (ภาษาไทย)",
        "example": {
            "ชื่อ Account": "นางสาว พิมพ์พิชา ใจดี",
            "ที่อยู่":"บ้านเลขที่ 45/7 ถ.พัฒนา ซอยจงใจ ต.ในเมือง อ.เมือง จ.เชียงใหม่ รหัสไปรษณีย์ 50000",
            "ข้อมูลที่ขอความช่วยเหลือ": "ต้องการอาหารและน้ำดื่มสำหรับครอบครัว 4 คน เนื่องจากบ้านถูกน้ำท่วม",
            "ประเภทความช่วยเหลือ": "อาหาร",
            "เบอร์โทร": ["0812345678", "+66891234567"],
            "เวลาที่สะดวกติดต่อ": "09:00-18:00",
            "ฉุกเฉิน": True
        },
        "constraints": {
            "ชื่อ Account": "string, min 0 char, max 200",
            "ที่อยู่": "string",
            "ข้อมูลที่ขอความช่วยเหลือ": "string",
            "ประเภทความช่วยเหลือ": "enum: ['การแพทย์','การเงิน','ที่พักอาศัย','อาหาร','กฎหมาย/ปรึกษา','อื่นๆ']",
            "เบอร์โทร": "array of string, regex ^(?:\\+66|0)\\d{8,9}$",
            "เวลาที่สะดวกติดต่อ": "string, optional",
            "ฉุกเฉิน": "boolean"
        }
    }

    return schema

        
def image_base64(image_path):
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
        
    return image_base64


def main():
    image_path = r"C:\Users\praejirapa\Pictures\588497508_26033068199629460_2091224368113351131_n.jpg"
    # image_base64 = image_base64(image_path)
    result = classify_and_content(image_path)

    # print(result)
    # print(result['ที่อยู่'])
    # print(type(result))
    return result

if __name__=="__main__":
    output = main()
    print(output)