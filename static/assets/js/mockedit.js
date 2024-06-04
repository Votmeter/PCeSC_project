document.addEventListener('DOMContentLoaded', function() {
    fetchCollectionDocuments();

    document.getElementById('save-button').addEventListener('click', saveDocument);
});

async function fetchCollectionDocuments() {
    const params = new URLSearchParams(window.location.search);
    const collectionName = params.get('collection');

    if (collectionName) {
        try {
            const response = await fetch(`/get_documents/${collectionName}`);
            if (!response.ok) throw new Error('Errore nel recupero dei documenti');
            const documents = await response.json();
            populateDocumentSelect(documents);
            document.getElementById('collection-name').value = collectionName;
        } catch (error) {
            alert(error.message);
        }
    }
}

function populateDocumentSelect(documents) {
    const documentSelect = document.getElementById('document-select');
    for (const [docId, docData] of Object.entries(documents)) {
        const option = document.createElement('option');
        option.value = docId;
        option.text = docId;
        documentSelect.appendChild(option);
    }
}

function loadDocument() {
    const documentSelect = document.getElementById('document-select');
    const selectedDocId = documentSelect.value;
    const collectionName = document.getElementById('collection-name').value;

    if (selectedDocId) {
        fetch(`/get_document/${collectionName}/${selectedDocId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('document-content').value = JSON.stringify(data, null, 2);
            })
            .catch(error => alert('Errore nel caricamento del documento: ' + error.message));
    } else {
        document.getElementById('document-content').value = '';
    }
}

async function saveDocument() {
    const collectionName = document.getElementById('collection-name').value;
    const documentSelect = document.getElementById('document-select');
    const selectedDocId = documentSelect.value;
    const documentContent = document.getElementById('document-content').value;

    if (!selectedDocId) {
        alert('Seleziona un documento da salvare.');
        return;
    }

    try {
        JSON.parse(documentContent);  // Validazione JSON
    } catch (error) {
        alert('Errore nel formato JSON.');
        return;
    }

    try {
        const response = await fetch(`/update_document/${collectionName}/${selectedDocId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: documentContent
        });

        if (response.ok) {
            alert('Documento aggiornato con successo!');
        } else {
            alert('Errore nell\'aggiornamento del documento.');
        }
    } catch (error) {
        alert('Errore durante l\'invio dei dati al server.');
    }
}
