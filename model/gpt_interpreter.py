from transformers import AutoModelForCausalLM, AutoTokenizer


MAX_LENGTH = 64

class GPTInterpreter:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def interpret_text(self, text):
        inputs = self.tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=MAX_LENGTH)
        
        outputs = self.model.generate(
            inputs,
            max_length=MAX_LENGTH,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )

        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        answer = full_text[len(text):].strip()

        return answer
