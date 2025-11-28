from ocr_test import classify_and_content
import gradio as gr
import traceback, json

def result_all(image_path):
    try:
        result = classify_and_content(image_path)
        return result
    except Exception as e:
        return json.loads(str(e))


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath")
            with gr.Row():
                btn_clear = gr.ClearButton(components=[image_input])
                btn = gr.Button("Submit", variant="primary") # กำหนด variant="primary" เพื่อให้ปุ่มเป็นสีของธีม
            
        json_output = gr.JSON(label="Information")
        
    gr.Markdown("Seperate Information")
    
    with gr.Row():
        with gr.Column():
            acc_name = gr.Textbox(label="ชื่อผู้แจ้งเหตุ")
            address = gr.Textbox(label="ที่อยู่")
        with gr.Column():
            info = gr.TextArea(label="ข้อมูลที่ขอความช่วยเหลือ")
            type_help = gr.Textbox(label="ประเภทความช่วยเหลือ")
        with gr.Column():
            call = gr.Textbox(label="เบอร์โทร")
            emer = gr.Textbox(label="ฉุกเฉิน")
    
    def process(image_path):
        if image_path is None:
            gr.Warning("รูปภาพไม่ถูกต้อง")
        
        try:
            result_json = result_all(image_path)
            acc_name = result_json["ชื่อ Account"]
            address = result_json["ที่อยู่"]
            info = result_json["ข้อมูลที่ขอความช่วยเหลือ"]
            type_help = result_json["ประเภทความช่วยเหลือ"]
            call = " "
            for c in result_json["เบอร์โทร"]:
                call = call +", "+ c
            emer = result_json["ฉุกเฉิน"]
            
            return result_json, acc_name, address, info, type_help, call, emer
        except Exception as e:
            # error_msg = str(e)
            error_msg = "ไม่พบข้อมูล"
            return {error_msg}, error_msg, error_msg, error_msg, error_msg, error_msg, error_msg
    
    try:
        btn.click(
            fn=process,
            inputs=image_input,
            outputs=[json_output, acc_name, address, info, type_help, call, emer]
        )
    except Exception as e:
        gr.Warning("รูปภาพไม่ถูกต้อง")
        gr.Error("รูปภาพไม่ถูกต้อง")
    
    btn_clear.click()
        
demo.launch(
    theme=gr.themes.Soft(),
    share=True
)

    