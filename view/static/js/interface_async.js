document.addEventListener('DOMContentLoaded', () => {

    // --- Referências do DOM ---
    const form = document.getElementById('template-form');
    const descriptionInput = document.getElementById('description');
    const jsonInput = document.getElementById('json-input');
    const jsonOutput = document.getElementById('json-output');
    const formError = document.getElementById('form-error');
    const cardContainer = document.getElementById('card-container');
    
    // Referências para o visualizador de template
    const templateResultContainer = document.getElementById('template-result');
    const templateResultCode = templateResultContainer.querySelector('code');

    // URL da sua API
    const API_BASE_URL = 'http://127.0.0.1:8000';

    // Variável para rastrear qual card está sendo exibido
    let activeCardId = null;

    // --- Ouvinte do Formulário ---
    form.addEventListener('submit', handleFormSubmit);

    /**
     * Lida com o envio do formulário.
     */
    async function handleFormSubmit(event) {
        event.preventDefault(); 
        clearErrors();

        let inputData, outputData;

        // 1. Validar JSONs de entrada
        try {
            inputData = JSON.parse(jsonInput.value);
        } catch (e) {
            showError('O JSON de Entrada (Input) é inválido.');
            return;
        }

        try {
            outputData = JSON.parse(jsonOutput.value);
        } catch (e) {
            showError('O JSON de Saída (Output) é inválido.');
            return;
        }

        const description = descriptionInput.value || 'Novo Processamento';

        // 2. Montar corpo da requisição POST
        const body = {
            description: description,
            input: inputData,
            output: outputData
        };

        // 3. Chamar a API POST
        try {
            const response = await fetch(`${API_BASE_URL}/template/resolve/async`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'WebApp-Gerador-Template'
                },
                body: JSON.stringify(body)
            });

            const data = await response.json();

            // 4. Lidar com a resposta (esperado 202)
            if (response.status === 202) {
                addProcessingCard(data.processingId, description);
                descriptionInput.value = '';
                jsonInput.value = '';
                jsonOutput.value = '';
            } else {
                showError(`Erro da API: ${data.message || response.statusText}`);
            }

        } catch (error) {
            console.error('Erro ao chamar API de /resolve/async:', error);
            showError('Não foi possível conectar à API. Verifique o console.');
        }
    }

    /**
     * Adiciona um novo card de processamento na UI.
     */
    function addProcessingCard(processingId, description) {
        const card = document.createElement('div');
        card.className = 'template-card pending';
        card.dataset.processingId = processingId; 

        card.innerHTML = `
            <strong>${description}</strong>
            <div class="card-id">ID: ${processingId}</div>
            <small>Status: Pendente (Clique para verificar)</small>
        `;

        // Adiciona o ouvinte de clique para buscar ou exibir/ocultar
        card.addEventListener('click', handleCardClick);

        cardContainer.prepend(card); 
    }

    /**
     * Chamado ao clicar em um card.
     * Decide se deve buscar o template ou exibir/ocultar.
     */
    async function handleCardClick(event) {
        const card = event.currentTarget;
        
        if (card.classList.contains('completed')) {
            // Se já está completo, apenas exibe ou oculta
            toggleTemplateDisplay(card);
        } else if (!card.classList.contains('loading')) {
            // Se está pendente ou com erro (e não carregando), busca na API
            fetchTemplateResult(card);
        }
    }

    /**
     * Exibe ou oculta o visualizador de template.
     */
    function toggleTemplateDisplay(card) {
        const processingId = card.dataset.processingId;
        const smallStatus = card.querySelector('small');
        
        // Verifica se o card clicado é o que já está ativo
        const isActive = (templateResultContainer.style.display === 'block' && activeCardId === processingId);

        // Reseta o texto de todos os outros cards
        document.querySelectorAll('.template-card.completed').forEach(otherCard => {
            if (otherCard !== card) {
                otherCard.querySelector('small').textContent = 'Status: Concluído (Clique para ver)';
            }
        });

        if (isActive) {
            // --- Oculta o template ---
            templateResultContainer.style.display = 'none';
            activeCardId = null;
            smallStatus.textContent = 'Status: Concluído (Clique para ver)';
        } else {
            // --- Exibe o template ---
            // Pega o template armazenado no 'data-template' do card
            templateResultCode.textContent = card.dataset.template; 
            templateResultContainer.style.display = 'block';
            activeCardId = processingId;
            smallStatus.textContent = 'Status: Concluído (Clique para ocultar)';
        }
    }

    /**
     * Busca o resultado do template na API.
     */
    async function fetchTemplateResult(card) {
        const processingId = card.dataset.processingId;
        const smallStatus = card.querySelector('small');

        // Atualiza UI para estado de carregamento
        card.classList.add('loading');
        card.classList.remove('error'); // Limpa erro anterior, se houver
        smallStatus.textContent = 'Status: Buscando...';

        try {
            const response = await fetch(`${API_BASE_URL}/template/async/${processingId}`, {
                method: 'GET',
                headers: { 'User-Agent': 'WebApp-Gerador-Template' }
            });

            const data = await response.json();

            if (response.status === 200) {
                // --- Sucesso! ---
                // Armazena o template no próprio elemento do card
                card.dataset.template = data.template; 
                
                card.classList.remove('pending', 'loading', 'error');
                card.classList.add('completed');
                smallStatus.textContent = 'Status: Concluído (Clique para ver)';
            } else if (response.status === 404 || response.status === 202) { 
                // --- Ainda processando ---
                card.classList.remove('loading');
                smallStatus.textContent = 'Status: Ainda processando... (Clique para tentar de novo)';
            } else {
                // --- Outro erro da API ---
                throw new Error(data.message || 'Erro ao buscar dados');
            }

        } catch (error) {
            console.error('Erro ao buscar template:', error);
            card.classList.remove('pending', 'loading');
            card.classList.add('error');
            smallStatus.textContent = `Erro ao buscar. (Clique para tentar de novo)`;
        }
    }

    // --- Funções Auxiliares ---

    function showError(message) {
        formError.textContent = message;
        formError.style.display = 'block';
    }

    function clearErrors() {
        formError.textContent = '';
        formError.style.display = 'none';
    }
});