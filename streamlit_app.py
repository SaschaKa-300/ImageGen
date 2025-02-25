import streamlit as st
import replicate
from openai import OpenAI
import os

# Set up API clients
repl_client = replicate.Client(api_token=st.secrets["replicate_token"])
oai_client = OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Matthias Image Generator")
st.subheader("The trigger word for this model is 'MAPI'. Be sure to include it in your prompt.")
st.markdown('Example prompt "MAPI as head chef in a kitchen". [Example Output](https://replicate.delivery/xezq/2tE3tIhoQcKDDJAaO9yBcuT8t0kD82C9tpA70jo5Sppoie8JA/out-0.jpg)', unsafe_allow_html=True)
#st.markdown("12 Images will be generated by 6 different models.")

user_input = st.text_input("Enter your prompt:")


# List of different model versions
models = {
    "saschaka-300/matthias-model:9388b390fca72d01d157be9e1e2a4c4ec6664dde9c5b8c115a4432d919a68b79": "Model 1 (Classic)",
    "saschaka-300/matthias1:870e066ebab03a42b5e340a26d7ca2e1a2c6d23aeeb9c7713bc314cc4a423c35": "Model 2",
    #"saschaka-300/matthias2:1c0bd0f210fdc4f5377dddf0ad68c7c08f4ac93c5c0635eef09d713f9cd18c0d": "Model 3",
    #"saschaka-300/matthias3:c04ea86c96d1118f7adc6fd0fb63a8bad113b8066e52126952c254e4c9f29842": "Model 4",
    #"saschaka-300/matthias3morestepsandrank:ea0c55919c10a114b9760662e874e5b8dbdf25d624e6eae2de74b39222564c99": "Model 5 (same images as 4, but longer training)"
}


def generate_images(prompt, label):
    """ Generates images using all models and displays them immediately """
    st.markdown(f"### {label}")
    for model, alias in models.items():
        try:
            output = repl_client.run(
                model,
                input={
                    "model": "dev",
                    "prompt": prompt,
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
                image_url = str(output[0])
                st.image(image_url, caption=f"Generated Image with {alias}", use_container_width=True)
            else:
                st.error(f"Failed to generate image with {alias}.")

        except Exception as e:
            st.error(f"Error generating image with {alias}: {str(e)}")

def optimize_prompt(user_prompt):
    """ Optimizes a prompt using ChatGPT for photorealistic AI image generation """
    try:
        response = oai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """Optimize the following prompt for AI image generation. The goal is to make it highly photorealistic while keeping the essence of the original prompt.
                Some general tips:
                -be precise, detailed and direct
                -describe not only the content of the image but also such details as tone, style, color palette, and point of view,  
                -for photorealistic images, include the name of the device used (e.g., “shot on iPhone 16”), aperture, lens, and shot type.
                """},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error optimizing prompt: {str(e)}")
        return user_prompt  # Fallback to original prompt if API fails

if st.button("Generate"):
    with st.spinner("Generating images with original prompt..."):
        generate_images(user_input, "Original Prompt Results")

    with st.spinner("Optimizing prompt for photorealism..."):
        optimized_prompt = optimize_prompt(user_input)
        st.markdown(f"**Optimized Prompt:** {optimized_prompt}")

    with st.spinner("Generating images with optimized prompt..."):
        generate_images(optimized_prompt, "Optimized Prompt Results")

