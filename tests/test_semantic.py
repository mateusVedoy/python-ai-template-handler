
import numpy as np

from src.infraestructure.ai.semantic import AiSemantic


def test_find_relevant_chunks_happy_path(mocker):
    """
    Testa o cenário principal usando a fixture 'mocker' do pytest-mock.
    """

    mocker.patch('src.infraestructure.ai.semantic.os.getenv',
                 return_value='fake-model-name')

    mock_model_instance = mocker.MagicMock()

    prompt_embedding = np.array([[1.0, 0.0, 0.0]])
    mock_model_instance.encode.return_value = prompt_embedding

    mock_sentence_transformer_class = mocker.patch(
        'src.infraestructure.ai.semantic.SentenceTransformer')
    mock_sentence_transformer_class.return_value = mock_model_instance

    prompt = "Qual é o chunk mais relevante?"
    chunks = ["chunk_0", "chunk_1", "chunk_2"]
    embed_chunk = np.array([
        [0.1, 0.9, 0.0],  # Similaridade baixa
        [0.9, 0.1, 0.0],  # Similaridade alta (chunk_1)
        [0.5, 0.5, 0.0]   # Similaridade média
    ])

    semantic_search = AiSemantic()
    relevant_chunks = semantic_search.find_relevant_chunks(
        prompt, chunks, embed_chunk, top_k=2)

    assert relevant_chunks == ["chunk_1", "chunk_2"]

    mock_sentence_transformer_class.assert_called_once_with('fake-model-name')
    mock_model_instance.encode.assert_called_once_with(
        [prompt], convert_to_numpy=True)


def test_find_relevant_chunks_empty_list(mocker):
    """
    Testa o comportamento quando a lista de chunks de entrada é vazia.
    """

    mocker.patch('src.infraestructure.ai.semantic.os.getenv',
                 return_value='fake-model-name')
    mocker.patch('src.infraestructure.ai.semantic.SentenceTransformer')

    semantic_search = AiSemantic()
    relevant_chunks = semantic_search.find_relevant_chunks(
        "qualquer prompt", [], [])

    assert relevant_chunks == []


def test_find_relevant_chunks_top_k_greater_than_chunks(mocker):
    """
    Testa se todos os chunks são retornados (ordenados) quando top_k é muito grande.
    """

    mocker.patch('src.infraestructure.ai.semantic.os.getenv',
                 return_value='fake-model-name')

    mock_model_instance = mocker.MagicMock()
    mock_model_instance.encode.return_value = np.array([[1.0, 0.0, 0.0]])

    mocker.patch('src.infraestructure.ai.semantic.SentenceTransformer',
                 return_value=mock_model_instance)

    prompt = "Qualquer"
    chunks = ["chunk_A", "chunk_B"]
    embed_chunk = np.array([
        [0.1, 0.9, 0.0],  # chunk_A (baixa similaridade)
        [0.9, 0.1, 0.0],  # chunk_B (alta similaridade)
    ])

    # Act
    semantic_search = AiSemantic()

    relevant_chunks = semantic_search.find_relevant_chunks(
        prompt, chunks, embed_chunk, top_k=5)

    assert len(relevant_chunks) == 2
    assert relevant_chunks == ["chunk_B", "chunk_A"]
