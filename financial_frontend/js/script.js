/***************************************************************************************
* Constantes e Configurações                                                           *    
****************************************************************************************/ 
const API_BASE_URL = 'http://localhost:5000';
const CACHE_EXPIRATION = 60000;

// Mapeamento de endpoints para tabelas
const ENDPOINT_MAPPINGS = [
    { pattern: 'home', cacheKey: 'home', tableId: 'home-items-table', isHome: true },
    { pattern: 'category', cacheKey: 'category', tableId: 'category-items-table' },
    { pattern: 'bank', cacheKey: 'bank', tableId: 'bank-items-table' },
    { pattern: 'branch', cacheKey: 'branch', tableId: 'branch-items-table' },
    { pattern: 'resource', cacheKey: 'resource', tableId: 'resource-items-table' },
    { pattern: 'account', cacheKey: 'account', tableId: 'account-items-table' },
    { pattern: 'transaction', cacheKey: 'transaction', tableId: 'transaction-items-table' }
];

/***************************************************************************************
* Cache de elementos DOM                                                               *    
****************************************************************************************/ 
const elements = {
    navButtons: document.querySelectorAll('.nav-button'),
    pages: document.querySelectorAll('.page'),
    messageElement: document.getElementById('message-area'),
    searchInputs: {
        category: document.getElementById('category-search'),
        bank: document.getElementById('bank-search'),
        branch: document.getElementById('branch-search'),
        resource: document.getElementById('resource-search'),
        account: document.getElementById('account-search'),
        transaction: document.getElementById('transaction-search')
    },
    addButtons: {
        category: document.querySelector('#category-form .btn-add'),
        bank: document.querySelector('#bank-form .btn-add'),
        branch: document.querySelector('#branch-form .btn-add'),
        resource: document.querySelector('#resource-form .btn-add'),
        account: document.querySelector('#account-form .btn-add'),
        transaction: document.querySelector('#transaction-form .btn-add')
    }
};

/***************************************************************************************
* Cache de dados da API                                                                *    
****************************************************************************************/
const apiCache = {
    lastUpdated: {},
    data: {        
        home: null,
        categories: null,
        banks: null,
        branches: null,
        resources: null,
        accounts: null,
        transactions: null}
};

/***************************************************************************************
* Fila de Operações                                                                   *    
****************************************************************************************/
const operationQueue = new Map();

/***************************************************************************************
* Funções utilitárias                                                                  *    
****************************************************************************************/
function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

function showMessage(message, type = 'info') {
    const element = elements.messageElement;
    element.textContent = message;
    element.className = `message-area ${type}`;
    element.style.display = 'block';
    element.style.opacity = "1";
    element.style.transform = 'translateX(0)';
    
    setTimeout(() => {
        element.style.opacity = '0';
        element.style.transform = 'translateX(100)';
        setTimeout(() => { 
            element.style.display = 'none';
        }, 500)
    }, 5000);
}

async function enqueueOperation(entityType, operation) {
    if (!operationQueue.has(entityType)) {
        operationQueue.set(entityType, Promise.resolve());
    }

    const queue = operationQueue.get(entityType);
    operationQueue.set(entityType, queue.then(operation).catch(() => {}));
    return operationQueue.get(entityType);
}
/***************************************************************************************
* Funções de manipulação de dados genéricas                                           *
****************************************************************************************/
function formatFieldValue(value, type) {
    if (value === undefined || value === null) return '';
    
    switch(type) {
        case 'date':
            return new Date(value).toLocaleDateString('pt-BR');
        case 'currency':
            return parseFloat(value).toFixed(2);
        case 'boolean':
            return value ? 'Sim' : 'Não';
        default:
            return value.toString();
    }
}

function getFieldsForEntity(entityType) {
    const fieldsMap = {
        home: [
            { key: 'transaction_date', type: 'date', align: 'center' },
            { key: 'transaction_description', type: 'text' },
            { key: 'category_id', type: 'text', align: 'center' },
            { key: 'transaction_value', type: 'currency', align: 'right' },
            { key: 'transaction_type', type: 'text', align: 'center' }
        ],
        category: [
            { key: 'category_id', type: 'text', align: 'center' },
            { key: 'category_description', type: 'text' },
            { key: 'category_type', type: 'text', align: 'center' }
        ],
        bank: [
            { key: 'bank_id', type: 'text', align: 'right' },
            { key: 'bank_description', type: 'text' },
            { key: 'bank_ispb', type: 'text', align: 'center' },
            { key: 'bank_type', type: 'text', align: 'center' }
        ],
        branch: [
            { key: 'bank_id', type: 'text', align: 'right' },
            { key: 'branch_id', type: 'text', align: 'right' },
            { key: 'branch_description', type: 'text', align: 'center' },
            { key: 'branch_cep', type: 'text', align: 'center' },
            { key: 'branch_address', type: 'text' },
            { key: 'branch_number', type: 'text', align: 'center' },
            { key: 'branch_complement', type: 'text' },
            { key: 'branch_district', type: 'text', align: 'center' },
            { key: 'branch_city', type: 'text', align: 'center' },
            { key: 'branch_state', type: 'text', align: 'center' },
            { key: 'branch_country', type: 'text' },
            { key: 'branch_phone', type: 'text', align: 'right' },
            { key: 'branch_email', type: 'text', align: 'center' }
        ],
        resource: [
            { key: 'resource_id', type: 'text', align: 'center' },
            { key: 'resource_description', type: 'text' },
            { key: 'resource_status', type: 'text', align: 'center' }
        ],
        account: [
            { key: 'account_id', type: 'text', align: 'right' },
            { key: 'branch_id', type: 'text', align: 'right' },
            { key: 'resource_id', type: 'text', align: 'center' }
        ],
        transaction: [
            { key: 'transaction_id', type: 'text', align: 'right' },
            { key: 'transaction_date', type: 'date', align: 'center' },
            { key: 'transaction_expiration_date', type: 'date', align: 'center' },
            { key: 'transaction_description', type: 'text' },
            { key: 'category_id', type: 'text', align: 'center', excludeFromPayLoad: true },
            { key: 'account_id', type: 'text', align: 'center' },
            { key: 'branch_id', type: 'text', align: 'center' },
            { key: 'resource_id', type: 'text', align: 'center' },
            { key: 'transaction_type', type: 'text', align: 'center' },
            { key: 'transaction_value', type: 'currency', align: 'right' },
            { key: 'transaction_status', type: 'text', align: 'center' }
        ]
    };
    
    return fieldsMap[entityType] || [];
}

function createTableRow(item, entityType) {
    const row = document.createElement('tr');
    const fields = getFieldsForEntity(entityType);
    
    fields.forEach(field => {
        const cell = document.createElement('td');
        cell.textContent = formatFieldValue(item[field.key], field.type);
        cell.classList.add(`align-${field.align}`);
        row.appendChild(cell);
    });

    // Célula de ações
    const actionCell = document.createElement('td');
    actionCell.className = 'action-cell';
    actionCell.innerHTML = `
        <span class="span-delete">
            <img class="btn-delete" src="imagens/trash.png" alt="Excluir">
        </span>
    `;
    row.appendChild(actionCell);

    return row;
}

/***************************************************************************************
* Operações CRUD genéricas                                                             *
****************************************************************************************/
async function fetchData(url, method = 'GET', body = null) {
    if (!navigator.onLine) {
        showMessage('Sem conexão com a internet', 'error');
        throw new Error('Offline');
    }

    try {
        const startTime = performance.now();
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        
        if (body) options.body = JSON.stringify(body);
            
        const response = await fetch(url, options);
        console.log(`${method} ${url} took ${performance.now() - startTime}ms`);
        
        if (!response.ok) {
            if (response.status === 422) {
                const errorData = await response.json();
                console.error("Erro 422 - Dados inválidos:", errorData);
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error in ${method} request to ${url}`, error);
        throw error;
    }
}

async function fetchWithRetry(url, options, retries = 3) {
    try {
        return await fetchData(url, options.method, options.body);
    } catch (error) {
        if (retries > 0) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return fetchWithRetry(url, options, retries - 1);
        }
        throw error;
    }
}

async function createEntity(entityType, entityData) {
    return enqueueOperation(entityType, async () => {
        try {
            const response = await fetchWithRetry(`${API_BASE_URL}/${entityType}`, {
                method: 'POST',
                body: entityData
            });
            
            invalidateCache(entityType);
            showMessage(`${entityType} criado com sucesso!`, 'success');
            await refreshUI(entityType);
            return true;
        } catch (error) {
            showMessage(`Falha ao criar ${entityType}: ${error.message}`, 'error');
            return false;
        }
    });
}

async function updateEntity(entityType, entityId, updateData) {
    return enqueueOperation(entityType, async () => {
        try {
            if (!updateData || Object.keys(updateData).length === 0) {
                showMessage('Nenhum dado fornecido para atualização', 'warning');
                return false;
            }

            const payload = {
                [`${entityType}_id`]: entityId,
                ...updateData
            };

            const response = await fetchWithRetry(`${API_BASE_URL}/${entityType}`, {
                method: 'PATCH',
                body: payload
            });

            invalidateCache(entityType);
            showMessage(`${entityType} atualizado com sucesso!`, 'success');
            await refreshUI(entityType);
            return true;
        } catch (error) {
            showMessage(`Falha ao atualizar ${entityType}: ${error.message}`, 'error');
            return false;
        }
    });
}

async function deleteEntity(entityType, entityId) {
    return enqueueOperation(entityType, async () => {
        try {
            const response = await fetchWithRetry(`${API_BASE_URL}/${entityType}`, {
                method: 'DELETE',
                body: { [`${entityType}_id`]: entityId }
            });

            invalidateCache(entityType);
            showMessage(`${entityType} deletado com sucesso!`, 'success');
            await refreshUI(entityType);
            return true;
        } catch (error) {
            showMessage(`Falha ao deletar ${entityType}: ${error.message}`, 'error');
            return false;
        }
    });
}

function invalidateCache(entityType) {
    const cacheKey = entityType.endsWith('s') ? entityType : `${entityType}s`;
    apiCache.data[cacheKey] = null;
    apiCache.lastUpdated[cacheKey] = null;
}

async function refreshUI(entityType) {
    const mapping = ENDPOINT_MAPPINGS.find(m => m.cacheKey === entityType);
    if (!mapping) return;

    const activeButton = document.querySelector('.nav-button.active');
    if (activeButton && activeButton.getAttribute('data-endpoint').includes(entityType)) {
        await loadData(`${API_BASE_URL}${activeButton.getAttribute('data-endpoint')}`);
    }
}
/***************************************************************************************
* Funções de UI genéricas                                                             *
****************************************************************************************/
function getInputTypeForField(fieldType) {
    switch(fieldType) {
        case 'date': return 'date';
        case 'currency': return 'number';
        case 'boolean': return 'checkbox';
        default: return 'text';
    }
}

function addEditableRow(entityType) {
    toggleAddButtons(true);

    const tableMapping = ENDPOINT_MAPPINGS.find(m => m.cacheKey === `${entityType}`);
    if (!tableMapping?.tableId) {
        console.error(`Tabela não encontrada para ${entityType}`);
        toggleAddButtons(false);
        return;
    }

    const table = document.getElementById(tableMapping.tableId);
    if (!table) return;

    const existingEditRow = table.querySelector('tr input');
    if (existingEditRow) {
        showMessage('Conclua a edição atual antes de adicionar um novo item.', 'warning');
        return;
    }

    const row = table.insertRow();
    const fields = getFieldsForEntity(entityType);

    fields.forEach(field => {
        const cell = row.insertCell();
        if (field.excludeFromPayLoad) {
            cell.textContent = "Novo";
        } else {
            const input = document.createElement('input');
            input.type = getInputTypeForField(field.type);
            cell.appendChild(input);
        }
    });

    const actionCell = row.insertCell();
    actionCell.className = 'action-cell';
    
    // Cria container para os ícones
    const iconsContainer = document.createElement('div');
    iconsContainer.className = 'action-icons';

    // Ícone Salvar
    const saveSpan = document.createElement('span');
    saveSpan.className = 'span-save';
    const saveImg = document.createElement('img');
    saveImg.src = 'imagens/save.png';
    saveImg.className = 'btn-save';
    saveImg.alt = 'Salvar';
    saveImg.title = 'Salvar';
    saveSpan.appendChild(saveImg);
    saveImg.addEventListener('click', () => handleSaveRow(row, entityType));
    
    // Ícone Cancelar
    const cancelSpan = document.createElement('span');
    cancelSpan.className = 'span-cancel';
    const cancelImg = document.createElement('img');
    cancelImg.src = 'imagens/cancel.png';
    cancelImg.className = 'btn-cancel';
    cancelImg.alt = 'Cancelar';
    cancelImg.title = 'Cancelar';
    cancelSpan.appendChild(cancelImg);
    cancelImg.addEventListener('click', () => {
        row.remove();
        toggleAddButtons(false);
    });

    actionCell.appendChild(saveSpan);
    actionCell.appendChild(cancelSpan);
}

async function handleSaveRow(row, entityType) {
    const inputs = row.querySelectorAll('input, select');
    const fields = getFieldsForEntity(entityType).filter(f => !f.excludeFromPayLoad);
    const entityData = {};

    fields.forEach((field, index) => {
        if (field.excludeFromPayLoad) return; //Não ira levar os campos marcados par ao payload
        const input = inputs[index];
        let value = input.type === 'checkbox' ? input.checked : input.value;
        
        // Conversão de tipos
        switch(field.type) {
            case 'number':
            case 'currency':
                value = parseFloat(value);
                break;
            case 'boolean':
                value = Boolean(value);
                break;
        }
        
        entityData[field.key] = value;
    });

    try {
        const success = await createEntity(entityType, entityData);
        if (success) {
            replaceInputsWithValues(row, entityData, entityType);
            addDeleteButton(row, entityType, entityData[`${entityType}_id`]);
        }
    } catch (error) {
        console.error('Error saving row:', error);
    } finally {
        toggleAddButtons(false);
    }
}

function replaceInputsWithValues(row, entityData, entityType) {
    const fields = getFieldsForEntity(entityType);
    const cells = row.cells;

    fields.forEach((field, index) => {
        if (index >= cells.length - 1) return;
        
        const cell = cells[index];
        cell.textContent = formatFieldValue(entityData[field.key], field.type);
    });
}

function addDeleteButton(row, entityType, entityId) {
    const actionCell = row.cells[row.cells.length - 1];
    actionCell.innerHTML = '';
    
    const deleteSpan = document.createElement('span');
    deleteSpan.className = 'span-delete';
    
    const deleteImg = document.createElement('img');
    deleteImg.src = 'imagens/trash.png';
    deleteImg.className = 'btn-delete';
    deleteImg.alt = 'Excluir';
    
    deleteSpan.appendChild(deleteImg);
    actionCell.appendChild(deleteSpan);
    
    deleteImg.addEventListener('click', async (e) => {
        e.stopPropagation();
        if (confirm('Você tem certeza que deseja excluir este item?')) {
            const success = await deleteEntity(entityType, entityId);
            if (success) row.remove();
        }
    });
}

function enableCellEditing(cell) {
    const originalContent = cell.textContent.trim();
    const row = cell.parentElement;
    const entityType = getEntityTypeFromTable(row.closest('table'));
    const fieldIndex = cell.cellIndex;
    const fields = getFieldsForEntity(entityType);
    const fieldType = fields[fieldIndex]?.type || 'text';

    const input = document.createElement('input');
    input.type = getInputTypeForField(fieldType);
    input.value = originalContent;
    input.className = 'edit-input';

    cell.textContent = '';
    cell.appendChild(input);
    input.focus();

    input.addEventListener('blur', () => finishEditing(cell, input, originalContent, entityType, row));
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            finishEditing(cell, input, originalContent, entityType, row);
        } else if (e.key === 'Escape') {
            cell.textContent = originalContent;
        }
    });
}

async function finishEditing(cell, input, originalContent, entityType, row) {
    const newValue = input.value.trim();
    cell.textContent = newValue || originalContent;

    if (newValue && newValue !== originalContent) {
        const entityId = row.cells[0].textContent.trim();
        const fieldIndex = cell.cellIndex;
        const fields = getFieldsForEntity(entityType);
        const fieldKey = fields[fieldIndex]?.key;

        if (fieldKey) {
            await updateEntity(entityType, entityId, { [fieldKey]: newValue });
        }
    }
}

/***************************************************************************************
* Funções de navegação e carregamento de dados                                        *
****************************************************************************************/
function handleNavigation(event) {
    const button = event.currentTarget;
    const pageId = button.getAttribute('data-page');
    const endpoint = button.getAttribute('data-endpoint');

    // Atualizar UI de navegação
    elements.navButtons.forEach(btn => btn.classList.remove('active'));
    elements.pages.forEach(page => {
        page.hidden = true;
        page.classList.remove('active');
    });

    button.classList.add('active');
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.hidden = false;
        targetPage.classList.add('active');
    }

    // Carregar dados se houver endpoint
    if (endpoint) {
        loadData(`${API_BASE_URL}${endpoint}`);
    }
}

async function loadData(url) {
    const match = ENDPOINT_MAPPINGS.find(mapping => url.includes(mapping.pattern));
    if (!match) {
        console.error(`Endpoint não mapeado: ${url}`);
        return;
    }

    const { cacheKey, tableId } = match;
    const table = document.getElementById(tableId);

    // Mostrar loading
    if (table) {
        const tbody = table.querySelector('tbody');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="100%">Carregando...</td></tr>';
        }
    }

    try {
        // Verificar cache
        if (apiCache.data[cacheKey] && 
            Date.now() - (apiCache.lastUpdated[cacheKey] || 0) < CACHE_EXPIRATION) {
            processData(apiCache.data[cacheKey], cacheKey, tableId);
            return;
        }

        const data = await fetchData(url);
        apiCache.data[cacheKey] = data;
        apiCache.lastUpdated[cacheKey] = Date.now();
        processData(data, cacheKey, tableId);
    } catch (error) {
        if (table) {
            const tbody = table.querySelector('tbody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="100%">Erro ao carregar dados</td></tr>';
            }
        }
        showMessage(`Falha ao carregar dados: ${error.message}`, 'error');
    }
}

function processData(data, cacheKey, tableId) {
    const items = Array.isArray(data) ? data : data[cacheKey] || data.detalhes?.[cacheKey] || [];
    
    if (!items.length) {
        showMessage(`Nenhum dado encontrado para ${cacheKey}`, 'warning');
        return;
    }

    const table = document.getElementById(tableId);
    if (!table) {
        console.error(`Tabela ${tableId} não encontrada`);
        return;
    }

    const tbody = table.querySelector('tbody');
    if (!tbody) {
        console.error(`Corpo da tabela ${tableId} não encontrado`);
        return;
    }

    // Implementação básica de virtual scrolling
    tbody.innerHTML = '';
    const renderChunk = (start, end) => {
        const fragment = document.createDocumentFragment();
        items.slice(start, end).forEach(item => {
            fragment.appendChild(createTableRow(item, cacheKey));
        });
        tbody.appendChild(fragment);
    };

    // Renderiza os primeiros 50 itens
    renderChunk(0, Math.min(50, items.length));

    // Configura scroll listener para carregar mais itens
    if (items.length > 50) {
        let loading = false;
        table.addEventListener('scroll', () => {
            if (!loading && table.scrollTop + table.clientHeight >= table.scrollHeight - 100) {
                loading = true;
                const currentCount = tbody.querySelectorAll('tr').length;
                if (currentCount < items.length) {
                    renderChunk(currentCount, Math.min(currentCount + 50, items.length));
                }
                loading = false;
            }
        });
    }

    setupEventDelegation();
}

/***************************************************************************************
* Funções específicas para a Home                                                     *
****************************************************************************************/
async function loadHomeData() {
  try {
    // Obter o mês e ano atual
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth() + 1;
    const currentYear = currentDate.getFullYear();
    
    // Carregar transações do mês atual
    //const transactions = await fetchData(`${API_BASE_URL}/transactions?month=${currentMonth}&year=${currentYear}`);
    
    // Processar os dados
    //processHomeData(transactions);
  } catch (error) {
    showMessage(`Falha ao carregar dados da home: ${error.message}`, 'error');
  }
}

function processHomeData(transactions) {
  if (!transactions || transactions.length === 0) {
    showMessage('Nenhuma transação encontrada para o mês atual', 'info');
    return;
  }

  // Agrupar transações por categoria
  const categoriesSummary = {};
  let totalIncome = 0;
  let totalExpenses = 0;

  transactions.forEach(transaction => {
    const category = transaction.category_id || 'Sem Categoria';
    const amount = parseFloat(transaction.transaction_value);
    const type = transaction.transaction_type;

    if (!categoriesSummary[category]) {
      categoriesSummary[category] = {
        income: 0,
        expenses: 0,
        transactions: []
      };
    }

    if (type === 'income') {
      categoriesSummary[category].income += amount;
      totalIncome += amount;
    } else {
      categoriesSummary[category].expenses += amount;
      totalExpenses += amount;
    }

    categoriesSummary[category].transactions.push(transaction);
  });

  // Atualizar os cards de resumo
  document.getElementById('total-income').textContent = `R$ ${totalIncome.toFixed(2)}`;
  document.getElementById('total-expenses').textContent = `R$ ${totalExpenses.toFixed(2)}`;
  document.getElementById('balance').textContent = `R$ ${(totalIncome - totalExpenses).toFixed(2)}`;

  // Criar gráfico de categorias
  renderCategoriesChart(categoriesSummary);

  // Criar gráfico de evolução mensal (simplificado)
  renderMonthlyTrendChart(transactions);

  // Preencher tabela de transações recentes
  renderRecentTransactions(transactions);
}

function renderCategoriesChart(categoriesData) {
  const ctx = document.getElementById('categories-chart').getContext('2d');
  
  // Preparar dados para o gráfico
  const labels = Object.keys(categoriesData);
  const incomeData = labels.map(label => categoriesData[label].income);
  const expensesData = labels.map(label => categoriesData[label].expenses);

  // Destruir gráfico anterior se existir
  if (window.categoriesChart) {
    window.categoriesChart.destroy();
  }

  window.categoriesChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Receitas',
          data: incomeData,
          backgroundColor: '#4caf50',
          borderColor: '#2e7d32',
          borderWidth: 1
        },
        {
          label: 'Despesas',
          data: expensesData,
          backgroundColor: '#f44336',
          borderColor: '#c62828',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function renderMonthlyTrendChart(transactions) {
  const ctx = document.getElementById('monthly-trend-chart').getContext('2d');
  
  // Agrupar por dia (simplificado)
  const dailySummary = {};
  transactions.forEach(transaction => {
    const date = new Date(transaction.transaction_date);
    const day = date.getDate();
    
    if (!dailySummary[day]) {
      dailySummary[day] = {
        income: 0,
        expenses: 0
      };
    }
    
    const amount = parseFloat(transaction.transaction_value);
    if (transaction.transaction_type === 'income') {
      dailySummary[day].income += amount;
    } else {
      dailySummary[day].expenses += amount;
    }
  });
  
  // Preparar dados
  const days = Object.keys(dailySummary).sort();
  const incomeTrend = days.map(day => dailySummary[day].income);
  const expensesTrend = days.map(day => dailySummary[day].expenses);

  // Destruir gráfico anterior se existir
  if (window.monthlyTrendChart) {
    window.monthlyTrendChart.destroy();
  }

  window.monthlyTrendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: days.map(day => `Dia ${day}`),
      datasets: [
        {
          label: 'Receitas',
          data: incomeTrend,
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          tension: 0.1,
          fill: true
        },
        {
          label: 'Despesas',
          data: expensesTrend,
          borderColor: '#f44336',
          backgroundColor: 'rgba(244, 67, 54, 0.1)',
          tension: 0.1,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function renderRecentTransactions(transactions) {
  const tbody = document.querySelector('#recent-transactions tbody');
  tbody.innerHTML = '';

  // Ordenar por data (mais recente primeiro)
  const sortedTransactions = [...transactions].sort((a, b) => 
    new Date(b.transaction_date) - new Date(a.transaction_date)
  );

  // Mostrar apenas as 10 mais recentes
  const recentTransactions = sortedTransactions.slice(0, 10);

  recentTransactions.forEach(transaction => {
    const row = document.createElement('tr');
    
    const dateCell = document.createElement('td');
    dateCell.textContent = new Date(transaction.transaction_date).toLocaleDateString('pt-BR');
    dateCell.classList.add('align-center');
    row.appendChild(dateCell);
    
    const descCell = document.createElement('td');
    descCell.textContent = transaction.transaction_description;
    row.appendChild(descCell);
    
    const categoryCell = document.createElement('td');
    categoryCell.textContent = transaction.category_id || 'Sem Categoria';
    row.appendChild(categoryCell);
    
    const valueCell = document.createElement('td');
    const value = parseFloat(transaction.transaction_value).toFixed(2);
    valueCell.textContent = `R$ ${value}`;
    valueCell.classList.add('align-right');
    valueCell.classList.add(transaction.transaction_type === 'income' ? 'positive-value' : 'negative-value');
    row.appendChild(valueCell);
    
    const typeCell = document.createElement('td');
    typeCell.textContent = transaction.transaction_type === 'income' ? 'Receita' : 'Despesa';
    typeCell.classList.add('align-center');
    row.appendChild(typeCell);
    
    tbody.appendChild(row);
  });
}

/***************************************************************************************
* Funções de busca e utilitários                                                      *
****************************************************************************************/
function searchTable(event) {
    const searchInput = event.target;
    const searchText = searchInput.value.trim().toLowerCase();
    const tableContainer = searchInput.closest('.search')?.nextElementSibling;
    const table = tableContainer?.querySelector('table');
    
    if (!table) {
        console.error('Tabela não encontrada para busca');
        return;
    }

    const rows = table.querySelectorAll('tbody tr');
    let matchesFound = false;

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let rowMatches = false;

        cells.forEach(cell => {
            if (cell.textContent.toLowerCase().includes(searchText)) {
                rowMatches = true;
            }
        });

        row.style.display = rowMatches ? '' : 'none';
        matchesFound = matchesFound || rowMatches;
    });

    if (!matchesFound && searchText.length > 0) {
        showMessage('Nenhum resultado encontrado para sua busca', 'warning');
    }
}

function getEntityTypeFromTable(table) {
    if (!table) return '';
    const tableId = table.id;
    const mapping = ENDPOINT_MAPPINGS.find(m => m.tableId === tableId);
    return mapping ? mapping.cacheKey : '';
}

/***************************************************************************************
* Configuração de eventos                                                             *
****************************************************************************************/
function setupEventDelegation() {
    // Remove event listeners antigos para evitar duplicação
    document.removeEventListener('click', handleDocumentClick);
    document.removeEventListener('dblclick', handleDocumentDblClick);

    // Adiciona os novos listeners
    document.addEventListener('click', handleDocumentClick);
    document.addEventListener('dblclick', handleDocumentDblClick);

    // Configura busca com debounce (mantido como está)
    Object.values(elements.searchInputs).forEach(input => {
        if (input) {
            input.addEventListener('input', debounce(searchTable));
        }
    });
}

// Função separada para lidar com clicks
function handleDocumentClick(e) {
    // Navegação
    if (e.target.classList.contains('nav-button')) {
        e.preventDefault();
        handleNavigation(e);
        return;
    }

    // Botão de adicionar
    if (e.target.classList.contains('btn-add') || e.target.closest('.btn-add')) {
        e.preventDefault();
        const button = e.target.classList.contains('btn-add') ? e.target : e.target.closest('.btn-add');
        const entityType = button.dataset.entityType;
        if (entityType) addEditableRow(entityType);
        return;
    }

    // Botão de deletar
    if (e.target.classList.contains('btn-delete')) {
        e.preventDefault();
        const row = e.target.closest('tr');
        const entityType = getEntityTypeFromTable(row.closest('table'));
        const entityId = row.cells[0].textContent;
        
        if (confirm('Você tem certeza?')) {
            deleteEntity(entityType, entityId).then(success => {
                if (success) row.remove();
            });
        }
        return;
    }

    // Botão de salvar
    if (e.target.classList.contains('btn-save')) {
        e.preventDefault();
        const row = e.target.closest('tr');
        const entityType = getEntityTypeFromTable(row.closest('table'));
        handleSaveRow(row, entityType);
        return;
    }

    // Botão de pesquisa
    if (e.target.classList.contains('btn-search')) {
        e.preventDefault();
        const searchInput = e.target.previousElementSibling;
        if (searchInput) searchTable({ target: searchInput });
        return;
    }
}

// Função separada para lidar com double clicks
function handleDocumentDblClick(e) {
    if (e.target.tagName === 'TD' && !e.target.classList.contains('action-cell')) {
        enableCellEditing(e.target);
    }
}

function toggleAddButtons(disabled = true) {
    document.querySelectorAll('.btn-add').forEach(button => {
        button.style.display = disabled ? 'none' : '';
        button.style.opacity = disabled ? 0.5 : 1;
        button.style.cursor = disabled ? 'not-allowed' : 'pointer'; 
    })
}

/***************************************************************************************
* Inicialização                                                                       *
****************************************************************************************/
function initialize() {
    // Configura eventos de navegação
    elements.navButtons.forEach(button => {
        button.addEventListener('click', handleNavigation);
    });

    // Configura a delegação do evento
    setupEventDelegation();

    // Carrega a página inicial
    const activeButton = document.querySelector('.nav-button.active') || 
                         document.querySelector('[data-page="home"]');
    if (activeButton) {
        const endpoint = activeButton.getAttribute('data-endpoint') || '/home';
        if (activeButton.getAttribute('data-page') === 'home-page') {
            loadHomeData();
        } else {
            loadData(`${API_BASE_URL}${endpoint}`);
        }
    }

    // Adicione o Chart.js se ainda não estiver carregado
    if (typeof Chart === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = () => console.log('Chart.js carregado');
        document.head.appendChild(script);
    }
}

// Inicia a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initialize);