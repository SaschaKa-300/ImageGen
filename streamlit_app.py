import streamlit as st
import replicate
import os

api = replicate.Client(api_token=st.secrets["replicate_token"])

st.title("Matthias Image Generator")
st.subheader("The trigger word for this model is MAPI. Be sure to include it in your prompt.")
st.markdown('Example prompt "MAPI as head chef in a kitchen". [Example Output](https://replicate.com/p/j28y7y6ta5rmc0ckpx9sp567fm)', unsafe_allow_html=True)

user_input = st.text_input("Enter your prompt:")

if st.button("Generate"):
    with st.spinner("Generating..."):
        output = api.run(
            "saschaka-300/matthias-model:9388b390fca72d01d157be9e1e2a4c4ec6664dde9c5b8c115a4432d919a68b79",
            input={
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
