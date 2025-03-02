import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

class MyStreamer:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def put(self, tokens):

        tokens = tokens[0]
        
        text = self.tokenizer.decode(tokens)

        if not text.startswith("<|") or not text.endswith("|>"):
            print(text, end="", flush=True)

    def end(self):
        pass

# Load model and tokenizer
MODEL_NAME = "microsoft/Phi-4-mini-instruct"

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
streamer = MyStreamer(tokenizer)

# Conversation history
conversation_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

def generate_response(user_input):
    global conversation_history
    
    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})
    
    # Format conversation history as context
    context = "\n".join(f"<|{turn['role']}|>{turn['content']}<|end|>" for turn in conversation_history)

    # Tokenize input
    input_ids = tokenizer(context, return_tensors="pt", truncation=True, max_length=2048).input_ids
    
    # Stream response token by token
    generated_tokens = []
    
    with torch.no_grad():
        output = model.generate(input_ids, max_new_tokens=200, temperature=.5, do_sample=True, streamer=streamer)
    
    print("\n")
    
    # Append model response to conversation history
    response_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    conversation_history.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        generate_response(user_input)
