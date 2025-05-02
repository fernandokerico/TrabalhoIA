document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById("fileDropzone");
    const previewContainer = document.getElementById("imagePreviewContainer");
    const noImageText = document.getElementById("noImageText");
    const submitButton = document.getElementById("submitDataBtn");
    const toggleRgbTrainConfigBtn = document.getElementById('toggleRgbTrainConfig');
    const rgbTrainConfigDiv = document.getElementById('rgbTrainConfig');
    const startTrainingBtn = document.getElementById("startTrainingBtn");
    const trainingStatus = document.getElementById("trainingStatus");
    const classFoldersInput = document.getElementById("classFolders");
    const classFoldersList = document.getElementById("classFoldersList");
    const classConfigsContainer = document.getElementById("classConfigsContainer");
    const addClassButton = document.getElementById('addClassBtn');

    let classCounter = 0;
    const selectedClassFolders = [];

    // Inicialmente esconde a seção de configuração detalhada do treinamento RGB
    if (rgbTrainConfigDiv) {
        rgbTrainConfigDiv.classList.add('hidden');
    }

    // Adiciona um event listener ao botão de "Configurar Rede RGB"
    if (toggleRgbTrainConfigBtn && rgbTrainConfigDiv) {
        toggleRgbTrainConfigBtn.addEventListener('click', () => {
            rgbTrainConfigDiv.classList.toggle('hidden');
        });
    }

    if (addClassButton) {
        addClassButton.addEventListener('click', () => {
            classFoldersInput.click(); // Simula o clique no input de arquivo para selecionar pastas
        });
    }

    if (classFoldersInput) {
        classFoldersInput.addEventListener('change', (event) => {
            const files = event.target.files;
            if (files.length > 0) {
                console.log("Número de itens selecionados:", files.length);
                const potentialClasses = {};

                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    console.log("Item:", file.name, "Tipo:", file.type, "Caminho:", file.webkitRelativePath);

                    const pathParts = file.webkitRelativePath ? file.webkitRelativePath.split('/') : [file.name];
                    if (pathParts.length > 1) {
                        const className = pathParts[0];
                        if (!potentialClasses[className]) {
                            potentialClasses[className] = [];
                        }
                        potentialClasses[className].push(file);
                    } else if (pathParts.length === 1 && file.type === "") {
                        // Detecta a "pasta" desktop.ini (ou similar sem tipo) como uma classe
                        const className = file.name;
                        if (!potentialClasses[className]) {
                            potentialClasses[className] = [];
                        }
                        potentialClasses[className].push(file);
                        console.log(">>>>> PASTA DETECTADA:", file.name);
                    } else {
                        console.log("Arquivo fora de uma pasta de classe:", file.name);
                        // Lidar com arquivos soltos, se necessário
                    }
                }

                console.log("Classes Potenciais Detectadas:", potentialClasses);

                for (const className in potentialClasses) {
                    if (!selectedClassFolders.some(folder => folder.name === className)) {
                        const fakeFolder = { name: className, isFakeFolder: true };
                        selectedClassFolders.push(fakeFolder);
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
            classFoldersInput.value = ''; // Limpa o input
        });
    }

    function addClassConfigSection(className, index) {
        const classConfigId = `classConfig-${index}`;
        const colorAttributesId = `colorAttributes-${index}`;
        const colorRangesId = `colorRanges-${index}`;
        const toleranceIdBase = `tolerance-${index}`;

        const classConfig = document.createElement('div');
        classConfig.className = 'class-config mb-4 p-4 border rounded relative'; // Adicionado 'relative' aqui
        classConfig.id = classConfigId; // Adiciona um ID único para a seção de configuração
        classConfig.innerHTML = `
            <h4 class="text-lg font-semibold text-gray-700 mb-2">Configurações para Classe: ${className}</h4>
            <div id="${colorAttributesId}">
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
                                <button type="button" class="removeFeatureBtn text-red-500 hover:text-red-700 focus:outline-none">
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
            </div>
        `;
        classConfigsContainer.appendChild(classConfig);
        attachColorPickerListeners(classConfig);
    }

    function removeActiveClassConfig(indexToRemove) {
        const classConfigToRemove = document.getElementById(`classConfig-${indexToRemove}`);
        if (classConfigToRemove) {
            const classNameToRemove = classConfigToRemove.querySelector('h4').textContent.split(': ')[1];
            const indexInSelected = selectedClassFolders.findIndex(folder => folder.name === classNameToRemove);
            if (indexInSelected > -1) {
                selectedClassFolders.splice(indexInSelected, 1);
                classCounter--;
                // Recarrega a lista de classes na interface
                classFoldersList.innerHTML = '';
                selectedClassFolders.forEach((folder, idx) => {
                    const listItem = document.createElement('div');
                    listItem.textContent = `Classe ${idx + 1}: ${folder.name} ${folder.isFakeFolder ? '(Detectada dos arquivos)' : ''}`;
                    classFoldersList.appendChild(listItem);
                });
            }
            classConfigToRemove.remove();
        }
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
                    <button type="button" class="removeFeatureBtn text-red-500 hover:text-red-700 focus:outline-none" onclick="this.parentNode.parentNode.parentNode.remove()">
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

        const removeButton = element.querySelector(".removeFeatureBtn");
        if (removeButton) {
            removeButton.addEventListener("click", () => {
                element.remove();
            });
        }
    }

    // Adicionar listeners para os color pickers existentes na carga da página (se houver)
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.class-config').forEach(attachColorPickerListeners);
    });

    if (startTrainingBtn) {
        startTrainingBtn.addEventListener('click', () => {
            if (selectedClassFolders.length < 2) {
                alert('Por favor, adicione pelo menos duas pastas de classes.');
                return;
            }

            const classConfigurations = [];
            selectedClassFolders.forEach((folder, index) => {
                const classIndex = index + 1;
                const colorRanges = [];
                const container = document.getElementById(`colorRanges-${classIndex}`);
                if (container) {
                    Array.from(container.children).forEach(rangeDiv => {
                        const rgbInput = rangeDiv.querySelector(".rgb-text");
                        const toleranceInput = rangeDiv.querySelector(`input[id^="tolerance-${classIndex}"]`);

                        if (rgbInput && toleranceInput) {
                            const rgbValues = rgbInput.value.split(',').map(v => parseInt(v.trim()));
                            if (rgbValues.length === 3 && rgbValues.every(Number.isInteger)) {
                                const tolerance = parseInt(toleranceInput.value);
                                colorRanges.push({
                                    target_rgb: rgbValues,
                                    tolerance: tolerance,
                                });
                            } else {
                                alert(`Por favor, insira valores RGB válidos para a classe ${folder.name}.`);
                                return;
                            }
                        }
                    });
                }
                classConfigurations.push({
                    class_name: folder.name,
                    color_ranges: colorRanges,
                });
            });

            if (classConfigurations.some(config => config.color_ranges.length === 0)) {
                alert('Por favor, defina pelo menos uma cor para cada classe.');
                return;
            }

            const trainingData = {
                class_configurations: classConfigurations,
                num_layers: 3, // Você pode adicionar campos para esses parâmetros no HTML
                neurons_per_layer: 64,
                num_epochs: 50,
                train_test_split: 0.8,
            };

            trainingStatus.textContent = 'Iniciando o treinamento...';

            fetch("/treinar_rgb_classes", { // Endpoint para treinamento com classes
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(trainingData),
            })
            .then(response => response.json())
            .then(data => {
                trainingStatus.textContent = `Treinamento concluído. Acurácia: ${data.accuracy || 'N/A'}`;
                localStorage.setItem('rgbModel', JSON.stringify(data.model)); // Salvar o modelo treinado
            })
            .catch(error => {
                console.error("Erro no treinamento:", error);
                trainingStatus.textContent = 'Erro ao iniciar o treinamento.';
            });
        });
    }

    if (dropzone) {
        dropzone.addEventListener("dragover", (event) => {
            event.preventDefault();
            dropzone.classList.add("active");
        });

        dropzone.addEventListener("dragleave", () => {
            dropzone.classList.remove("active");
        });

        dropzone.addEventListener("drop", (event) => {
            event.preventDefault();
            dropzone.classList.remove("active");
            previewImages(event.dataTransfer.files);
        });
    }

    function previewImages(files) {
        previewContainer.innerHTML = "";
        if (files.length > 0) {
            noImageText.style.display = "none";
        } else {
            noImageText.style.display = "block";
        }
        Array.from(files).forEach((file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.className = "preview-image";
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
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

            fetch("/processar", { // Revertendo para o endpoint antigo
                method: "POST",
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log("Resultado da classificação:", data);
                localStorage.setItem('analysisResults', JSON.stringify(data)); // Salvar no localStorage
                window.location.href = "/resultado"; // Redirecionar
            })
            .catch(error => {
                console.error("Erro na classificação:", error);
                alert("Ocorreu um erro ao classificar a imagem.");
            });
        });
    }
});