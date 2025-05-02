document.addEventListener('DOMContentLoaded', () => {
    const previewContainer = document.getElementById("imagePreviewContainer");
    const noImageText = document.getElementById("noImageText");
    const dropzone = document.getElementById("fileDropzone");
    const submitButton = document.getElementById("submitDataBtn");
    const toggleRgbTrainConfigBtn = document.getElementById('toggleRgbTrainConfig');
    const rgbTrainConfigDiv = document.getElementById('rgbTrainConfig');
    const startTrainingBtn = document.getElementById("startTrainingBtn");
    const trainingStatus = document.getElementById("trainingStatus");
    const classFoldersInput = document.getElementById("classFolders");
    const classFoldersList = document.getElementById("classFoldersList");
    const classConfigsContainer = document.getElementById("classConfigsContainer");
    const addClassButton = document.getElementById('addClassBtn');
    const closeTrainingBtnBottom = document.getElementById("closeTrainingBtn");
    const closeTrainingBtnTop = document.getElementById("closeRgbTrainConfigBtnTop");
    const fileInput = document.getElementById("fileInput");

    let classCounter = 0;
    const selectedClassFolders = [];

    if (rgbTrainConfigDiv) {
        rgbTrainConfigDiv.classList.add('hidden');
    }

    if (toggleRgbTrainConfigBtn && rgbTrainConfigDiv) {
        toggleRgbTrainConfigBtn.addEventListener('click', () => {
            rgbTrainConfigDiv.classList.toggle('hidden');
        });
    }

    if (closeTrainingBtnBottom && rgbTrainConfigDiv) {
        closeTrainingBtnBottom.addEventListener('click', () => {
            rgbTrainConfigDiv.classList.add('hidden');
        });
    }

    if (closeTrainingBtnTop && rgbTrainConfigDiv) {
        closeTrainingBtnTop.addEventListener('click', () => {
            rgbTrainConfigDiv.classList.add('hidden');
        });
    }

    if (addClassButton) {
        addClassButton.addEventListener('click', () => {
            classFoldersInput.click();
        });
    }

    if (classFoldersInput) {
        classFoldersInput.addEventListener('change', (event) => {
            const files = event.target.files;
            if (files.length > 0) {
                const potentialClasses = {};
                for (const file of files) {
                    const pathParts = file.webkitRelativePath ? file.webkitRelativePath.split('/') : [file.name];
                    const className = pathParts.length > 1 ? pathParts[0] : (pathParts.length === 1 && file.type === "" ? file.name : null);
                    if (className && !potentialClasses[className]) {
                        potentialClasses[className] = [];
                    }
                    if (className) {
                        potentialClasses[className].push(file);
                    }
                }

                for (const className in potentialClasses) {
                    if (!selectedClassFolders.some(folder => folder.name === className)) {
                        selectedClassFolders.push({ name: className, isFakeFolder: true });
                        classCounter++;
                        const listItem = document.createElement('div');
                        listItem.textContent = `Classe ${classCounter}: ${className} (Detectada dos arquivos)`;
                        classFoldersList.appendChild(listItem);
                        addClassConfigSection(className, classCounter);
                    } else {
                        alert(`A classe "${className}" já foi adicionada.`);
                    }
                }
            }
            classFoldersInput.value = '';
        });
    }

    function addClassConfigSection(className, index) {
        const classConfigId = `classConfig-${index}`;
        const colorRangesId = `colorRanges-${index}`;
        const toleranceIdBase = `tolerance-${index}`;

        const classConfig = document.createElement('div');
        classConfig.className = 'class-config mb-4 p-4 border rounded relative';
        classConfig.id = classConfigId;

        classConfig.innerHTML = `
            <h4 class="text-lg font-semibold text-gray-700 mb-2">Configurações para Classe: ${className}</h4>
            <div id="${colorRangesId}">
                <div class="feature-item">
                    <div class="grid md:grid-cols-12 gap-4 items-center">
                        <div class="md:col-span-5">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Cor RGB</label>
                            <div class="flex items-center">
                                <input type="color" value="#ff0000" class="mr-3 color-picker" data-class-index="${index}-1" />
                                <input type="text" value="255, 0, 0" class="rgb-text w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500" placeholder="R, G, B" data-class-index="${index}-1" />
                            </div>
                        </div>
                        <div class="md:col-span-2 text-right">
                            <button type="button" class="removeFeatureBtn text-red-500 hover:text-red-700 focus:outline-none" onclick="removeColorRange(this)">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                        <div class="md:col-span-12 mt-2">
                            <label for="${toleranceIdBase}-1" class="block text-sm font-medium text-gray-700 mb-1">Tolerância:</label>
                            <input type="number" id="${toleranceIdBase}-1" class="shadow-sm focus:ring-purple-500 focus:border-purple-500 block w-full sm:text-sm border-gray-300 rounded-md" value="10" min="0">
                        </div>
                    </div>
                </div>
            </div>
            <button type="button" class="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded mt-2" onclick="addColorRange(${index})">
                Adicionar Cor
            </button>
            <button type="button" class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none p-1 bg-none border-none cursor-pointer" onclick="removeActiveClassConfig(${index})">
                <i class="fas fa-times"></i>
            </button>
        `;
        classConfigsContainer.appendChild(classConfig);
        attachColorPickerListeners(classConfig);

        const removeButton = classConfig.querySelector('.absolute');
        if (removeButton) {
            removeButton.addEventListener('click', () => {
                removeActiveClassConfig(index);
            });
        }
    }

    function removeActiveClassConfig(indexToRemove) {
        console.log('Remover classe com índice:', indexToRemove);
        const classConfigToRemove = document.getElementById(`classConfig-${indexToRemove}`);
        console.log('Elemento a remover:', classConfigToRemove);
        if (classConfigToRemove) {
            const classNameToRemove = classConfigToRemove.querySelector('h4').textContent.split(': ')[1];
            const indexInSelected = selectedClassFolders.findIndex(folder => folder.name === classNameToRemove);
            if (indexInSelected > -1) {
                selectedClassFolders.splice(indexInSelected, 1);
                classCounter--;
                classFoldersList.innerHTML = '';
                selectedClassFolders.forEach((folder, idx) => {
                    const listItem = document.createElement('div');
                    listItem.textContent = `Classe ${idx + 1}: ${folder.name} ${folder.isFakeFolder ? '(Detectada dos arquivos)' : ''}`;
                    classFoldersList.appendChild(listItem);
                });
            }
            classConfigToRemove.remove();
            console.log('Classe removida com sucesso.');
        } else {
            console.warn(`Elemento classConfig-${indexToRemove} não encontrado.`);
        }
    }

    function attachColorPickerListeners(element) {
        const colorPicker = element.querySelector(".color-picker");
        const rgbText = element.querySelector(".rgb-text");
        if (colorPicker && rgbText) {
            colorPicker.addEventListener("input", () => {
                const hex = colorPicker.value;
                const r = parseInt(hex.slice(1, 3), 16);
                const g = parseInt(hex.slice(3, 5), 16);
                const b = parseInt(hex.slice(5, 7), 16);
                rgbText.value = `${r}, ${g}, ${b}`;
            });
        }
    }

    document.querySelectorAll('.class-config').forEach(attachColorPickerListeners);

    // Declare a função previewImages DENTRO do DOMContentLoaded
    function previewImages(files) {
        if (!previewContainer || !noImageText) {
            console.error("Erro: Elementos de pré-visualização não encontrados no DOM (dentro de previewImages).");
            return;
        }

        previewContainer.innerHTML = '';

        if (files && files.length > 0) {
            noImageText.style.display = 'none';
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const reader = new FileReader();

                reader.onload = function(e) {
                    const imgDiv = document.createElement('div');
                    imgDiv.className = 'relative';

                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'w-full h-auto rounded-md shadow-md';
                    imgDiv.appendChild(img);

                    const removeButton = document.createElement('button');
                    removeButton.innerHTML = '<i class="fas fa-times-circle text-red-500 hover:text-red-700 absolute top-1 right-1 bg-white rounded-full p-1"></i>';
                    removeButton.className = 'absolute top-0 right-0 focus:outline-none cursor-pointer';
                    removeButton.addEventListener('click', function() {
                        imgDiv.remove();
                        // Adicione aqui a lógica para remover o arquivo da lista de arquivos a serem enviados, se necessário
                    });
                    imgDiv.appendChild(removeButton);

                    previewContainer.appendChild(imgDiv);
                }
                reader.onerror = function() {
                    console.error("Erro ao ler o arquivo:", file.name);
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'text-red-500 text-sm italic';
                    errorDiv.textContent = `Erro ao pré-visualizar "${file.name}".`;
                    previewContainer.appendChild(errorDiv);
                };
                reader.readAsDataURL(file);
            }
        } else {
            noImageText.style.display = 'block';
        }
    }

    // Atribui o event listener ao fileInput DENTRO do DOMContentLoaded
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            previewImages(this.files);
        });
    }

    if (dropzone) {
        dropzone.addEventListener('drop', function(event) {
            event.preventDefault();
            this.classList.remove('active');
            previewImages(event.dataTransfer.files);
        });
    }

    if (submitButton) {
        submitButton.addEventListener("click", () => {
            const neuralType = document.querySelector('input[name="neuralType"]:checked').value;
            const analysisImages = document.getElementById("fileInput").files;

            if (analysisImages.length === 0) {
                alert('Por favor, selecione as imagens para análise.');
                return;
            }

            const formData = new FormData();
            formData.append("neuralType", neuralType);
            for (let i = 0; i < analysisImages.length; i++) {
                formData.append("images[]", analysisImages[i]);
            }

            fetch("/processar", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log("Resultado da classificação:", data);
                localStorage.setItem('analysisResults', JSON.stringify(data));
                window.location.href = "/resultado";
            })
            .catch(error => {
                console.error("Erro na classificação:", error);
                alert("Ocorreu um erro ao classificar a imagem.");
            });
        });
    }

    function addColorRange(classIndex) {
        const container = document.getElementById(`colorRanges-${classIndex}`);
        const rangeIndex = container.children.length + 1;
        const div = document.createElement('div');
        div.className = 'feature-item';
        div.innerHTML = `
            <div class="grid md:grid-cols-12 gap-4 items-center mt-4">
                <div class="md:col-span-5">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Cor RGB</label>
                    <div class="flex items-center">
                        <input type="color" value="#0000ff" class="mr-3 color-picker" data-class-index="${classIndex}-${rangeIndex}" />
                        <input type="text" value="0, 0, 255" class="rgb-text w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500" placeholder="R, G, B" data-class-index="${classIndex}-${rangeIndex}" />
                    </div>
                </div>
                <div class="md:col-span-2 text-right">
                    <button type="button" class="removeFeatureBtn text-red-500 hover:text-red-700 focus:outline-none" onclick="removeColorRange(this)">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
                <div class="md:col-span-12 mt-2">
                    <label for="tolerance-${classIndex}-${rangeIndex}" class="block text-sm font-medium text-gray-700 mb-1">Tolerância:</label>
                    <input type="number" id="tolerance-${classIndex}-${rangeIndex}" class="shadow-sm focus:ring-purple-500 focus:border-purple-500 block w-full sm:text-sm border-gray-300 rounded-md" value="10" min="0">
                </div>
            </div>
        `;
        container.appendChild(div);
        attachColorPickerListeners(div);
    }

    function removeColorRange(button) {
        const featureItem = button.parentNode.parentNode.parentNode;
        featureItem.remove();
    }
});

function attachColorPickerListeners(element) {
    const colorPicker = element.querySelector(".color-picker");
    const rgbText = element.querySelector(".rgb-text");
    if (colorPicker && rgbText) {
        colorPicker.addEventListener("input", () => {
            const hex = colorPicker.value;
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            rgbText.value = `${r}, ${g}, ${b}`;
        });
    }
}