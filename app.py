from flask import Flask, render_template, request
import base64

app = Flask(__name__)

# --- Dicionários e Funções de Conversão (sem alteração) ---
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ' ': '/'
}
MORSE_CODE_DECODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

def texto_para_binario(texto):
    return ' '.join(format(ord(char), '08b') for char in texto)

def binario_para_texto(binario):
    try:
        return ''.join(chr(int(byte, 2)) for byte in binario.split())
    except (ValueError, TypeError):
        return "Erro: Entrada binária inválida."

def texto_para_morse(texto): 
    texto = texto.upper()
    try:
        return ' '.join(MORSE_CODE_DICT[char] for char in texto)
    except KeyError as e:
        return f"Erro: O caractere '{e.args[0]}' não pode ser convertido para Morse."

def morse_para_texto(morse):
    return ''.join(MORSE_CODE_DECODE_DICT.get(code, '') for code in morse.split(' '))

def cifra_de_cesar(texto, chave, modo):
    alfabeto = 'abcdefghijklmnopqrstuvwxyz'
    resultado = ''
    if modo == 'descriptografar':
        chave = -chave
    for char in texto.lower():
        if char in alfabeto:
            posicao = alfabeto.find(char)
            nova_posicao = (posicao + chave) % 26
            resultado += alfabeto[nova_posicao]
        else:
            resultado += char
    return resultado

def texto_para_base64(texto):
    try:
        return base64.b64encode(texto.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"Erro ao codificar para Base64: {e}"

def base64_para_texto(b64_texto):
    try:
        return base64.b64decode(b64_texto.encode('utf-8')).decode('utf-8', errors='replace')
    except Exception as e:
        return f"Erro: Entrada Base64 inválida. {e}"


# --- Lógica do Flask ---
@app.route('/', methods=['GET', 'POST'])
def home():
    # Define valores padrão
    context = {
        'resultado': '',
        'texto_entrada': '',
        'tipo_conversao': 'txt2bin',
        'chave_cesar': 3
    }

    if request.method == 'POST':
        # Atualiza o contexto com os dados do formulário
        context['texto_entrada'] = request.form.get('texto_entrada', '')
        context['tipo_conversao'] = request.form.get('tipo_conversao')
        try:
            context['chave_cesar'] = int(request.form.get('chave_cesar', 3))
        except (ValueError, TypeError):
            context['chave_cesar'] = 3

        # Executa a conversão baseada na seleção
        texto = context['texto_entrada']
        opcao = context['tipo_conversao']
        chave = context['chave_cesar']

        if opcao == 'txt2bin': context['resultado'] = texto_para_binario(texto)
        elif opcao == 'bin2txt': context['resultado'] = binario_para_texto(texto)
        elif opcao == 'txt2morse': context['resultado'] = texto_para_morse(texto)
        elif opcao == 'morse2txt': context['resultado'] = morse_para_texto(texto)
        elif opcao == 'txt2b64': context['resultado'] = texto_para_base64(texto)
        elif opcao == 'b642txt': context['resultado'] = base64_para_texto(texto)
        elif opcao == 'cifrar_cesar': context['resultado'] = cifra_de_cesar(texto, chave, 'criptografar')
        elif opcao == 'decifrar_cesar': context['resultado'] = cifra_de_cesar(texto, chave, 'descriptografar')

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)