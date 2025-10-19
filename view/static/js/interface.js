// Seleciona os elementos do DOM
const form = document.getElementById('template-form');
const submitBtn = document.getElementById('submit-btn');
const descriptionInput = document.getElementById('description');
const inputJsonText = document.getElementById('input-json');
const outputJsonText = document.getElementById('output-json');
const statusMessage = document.getElementById('status-message');
const resultContainer = document.getElementById('result-container');
const resultTemplate = document.getElementById('result-template');

// Adiciona um listener para o evento de submit do formulário
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Impede o recarregamento da página

    // Reseta a interface para um novo envio
    submitBtn.disabled = true;
    submitBtn.textContent = 'Gerando...';
    statusMessage.style.display = 'none';
    resultContainer.style.display = 'none';
    statusMessage.className = '';

    let inputJson, outputJson;

    // 1. Valida o JSON de entrada
    try {
        inputJson = JSON.parse(inputJsonText.value);
    } catch (error) {
        showError('O JSON de Input é inválido. Por favor, verifique a formatação.');
        return;
    }

    // 2. Valida o JSON de saída
    try {
        outputJson = JSON.parse(outputJsonText.value);
    } catch (error) {
        showError('O JSON de Output é inválido. Por favor, verifique a formatação.');
        return;
    }

    // 3. Monta o corpo da requisição
    const requestBody = {
        description: descriptionInput.value,
        input: inputJson,
        output: outputJson
    };

    // 4. Envia a requisição para a API
    try {
        const response = await fetch('http://127.0.0.1:8000/template/resolve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            // Trata erros de HTTP (ex: 404, 500)
            throw new Error(`Erro na API: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // 5. Exibe o resultado com sucesso
        showSuccess(data.message);
        resultTemplate.textContent = data.template;
        resultContainer.style.display = 'block';

    } catch (error) {
        // Trata erros de rede ou da lógica da API
        showError(`Não foi possível conectar à API. Verifique se ela está rodando e acessível. Detalhes: ${error.message}`);
    } finally {
        // Reabilita o botão independentemente do resultado
        submitBtn.disabled = false;
        submitBtn.textContent = 'Gerar Template';
    }
});

// Funções auxiliares para exibir mensagens
function showMessage(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = type;
    statusMessage.style.display = 'block';
}

function showError(message) {
    showMessage(message, 'error');
    // Reabilita o botão em caso de erro de validação
    submitBtn.disabled = false;
    submitBtn.textContent = 'Gerar Template';
}

function showSuccess(message) {
    showMessage(message, 'success');
}