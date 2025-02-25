import streamlit as st
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "r8_6OOQ4A0PF8bz0Dg7ou4fuLPhsIU69Cm4HMZaT"
api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

st.title("My AI Model")

user_input = st.text_input("Enter your text:")

if st.button("Generate"):
    with st.spinner("Generating..."):
        output = api.run(
            "saschaka-300/matthias-model:9388b390fca72d01d157be9e1e2a4c4ec6664dde9c5b8c115a4432d919a68b79",
            input={
                "image": "https://w-gh.de/templates/yootheme/cache/wgl_wgh-223-6b6fdaaa.jpeg",
                "model": "dev",
                "prompt": user_input,
                "go_fast": False,
                "lora_scale": 1,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "guidance_scale": 3,
                "output_quality": 100,
                "prompt_strength": 0.81,
                "extra_lora_scale": 1,
                "num_inference_steps": 28
            }
        )
        
        if isinstance(output, list) and len(output) > 0:
            image_url = str(output[0])  # Ensure it's a string
            
            # Display the image
            st.image(image_url, caption="Generated Image", use_container_width=True)
        else:
            st.error("Failed to generate image. Please try again.")