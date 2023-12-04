from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


MAX_LENGTH = 64
USE_GPU = True

class GPTInterpreter:
    def __init__(self, model_name):
        self.device = 'cuda' if torch.cuda.is_available() and USE_GPU else 'cpu'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def interpret_text(self, text):
        inputs = self.tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=MAX_LENGTH)
        inputs = inputs.to(self.device)

        outputs = self.model.generate(
            inputs,
            max_length=MAX_LENGTH,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True,
            temperature=0.5,
            top_k=25,
            top_p=0.5
        )

        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        answer = full_text[len(text):].strip()

        return answer
