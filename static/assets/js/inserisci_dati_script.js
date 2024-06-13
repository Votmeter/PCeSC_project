// Funzione per ottenere i nomi delle collezioni dal backend
async function fetchCollections() {
  const response = await fetch("/get_collections");
  const collections = await response.json();
  const dropdown = document.getElementById("collections-dropdown");

  collections.forEach((collection) => {
    const option = document.createElement("option");
    option.text = collection;
    option.value = collection;
    dropdown.add(option);
  });
}

// async function fetchDocuments() {
//   const collectionName = event.target.value; // Get the selected value from the event object
//   const response = await fetch(`/get_documents/${collectionName}`);
//   const documents = await response.json();
//   const dropdown_li = document.getElementById("documents-dropdown");

//   documents.forEach((collection) => {
//     const option = document.createElement("option");
//     option.text = collection;
//     option.value = collection;
//     dropdown_li.add(option);
//   });
// }

async function fetchDocuments() {
  const collectionName = event.target.value; // Ottieni il valore selezionato dall'oggetto evento
  const response = await fetch(`/get_documents/${collectionName}`);
  const documents = await response.json();
  const dropdown_li = document.getElementById("documents-dropdown");

  // Svuota le opzioni esistenti
  dropdown_li.innerHTML = "";

  // Crea e aggiungi l'opzione "Seleziona coordinata"
  const defaultOption = document.createElement("option");
  defaultOption.text = "Seleziona coordinata";
  defaultOption.value = "";
  dropdown_li.add(defaultOption);

  // Aggiungi le nuove opzioni
  documents.forEach((collection) => {
    const option = document.createElement("option");
    option.text = collection;
    option.value = collection;
    dropdown_li.add(option);
  });
}

// Funzione per aggiungere una nuova collezione
async function addCollection() {
  const collectionName = document.getElementById("new-collection-name").value;
  const collectionData = document.getElementById("new-collection-json").value;

  try {
    const response = await fetch("/add_collection", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: collectionName,
        data: JSON.parse(collectionData),
      }),
    });

    if (response.ok) {
      alert("Collezione aggiunta con successo!");
      fetchCollections(); // Aggiorna la lista delle collezioni
    } else {
      alert("Errore nell'aggiunta della collezione.");
    }
  } catch (error) {
    alert("Errore nel formato JSON.");
  }
}

// Funzione per caricare un file JSON e popolare la textarea
function handleFileUpload(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function (event) {
    const content = event.target.result;
    document.getElementById("new-collection-json").value = content;
  };

  reader.readAsText(file);
}

async function updateDocumentDataText() {
  const collectionName = document.getElementById("collections-dropdown").value;
  const documentId = document.getElementById("documents-dropdown").value;

  try {
    const response = await fetch(`/${collectionName}/${documentId}`);
    if (!response.ok) {
      throw new Error("Errore nella caricazione del documento");
    }
    const content = await response.json();
    document.getElementById("update-collection-json").value = JSON.stringify(
      content,
      null,
      4
    );
  } catch (error) {
    alert("Errore nella caricazione del documento");
    console.error(error);
  }
}

async function updateCollection() {
  const collectionName = document.getElementById("collections-dropdown").value;
  const documentId = document.getElementById("documents-dropdown").value;
  const updatedContent = document.getElementById(
    "update-collection-json"
  ).value;

  try {
    const response = await fetch(`/${collectionName}/${documentId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: updatedContent,
    });

    if (!response.ok) {
      throw new Error("Errore nell'aggiornamento del documento");
    }

    const result = await response.json();
    if (result.success) {
      alert("Documento aggiornato con successo");
    } else {
      alert("Errore nell'aggiornamento del documento");
    }
  } catch (error) {
    alert("Errore nell'aggiornamento del documento");
    console.error(error);
  }
}

window.onload = fetchCollections;
