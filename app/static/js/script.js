const recordsPerPage = 10;
let currentPage = 1;

document.addEventListener('DOMContentLoaded', function () {
    $('#feedbackModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Botão que acionou o modal
        var feedbackId = button.data('feedback-id'); // Extrair o ID do feedback

        // Use Fetch API para obter os detalhes do feedback do servidor
        fetch(`/feedback/${feedbackId}`)
            .then(response => response.json())
            .then(data => {
                // Preencher o modal com os detalhes do feedback
                var modalBody = document.getElementById('feedbackDetails');
                if (modalBody) {
                    modalBody.innerHTML = `
                        <p><strong>ID:</strong> ${data.feedback_id}</p>
                        <p><strong>Feedback:</strong> ${data.feedback}</p>
                        <p><strong>Status:</strong> ${data.sentiment}</p>
                        <p><strong>Requested Features:</strong></p>
                        <ul>
                             ${data.requested_features.map(feature => 
                            `<li><strong>Code:</strong> ${feature.code}, <strong>Reason:</strong> ${feature.reasons}</li>`
                        ).join('')}
                        </ul>
                    `;
                } else {
                    console.error('Elemento com ID feedbackDetails não encontrado.');
                }
            })
            .catch(error => {
                console.error('Error fetching feedback details:', error);
            });
    });
    $('#feedbackModal').on('hidden.bs.modal', function () {
        var modalBody = document.getElementById('feedbackDetails');
        modalBody.innerHTML = ''; 
    });
    // Inicialização da tabela e gráficos
    changePage(1);

    const sentimentData = {
        x: feedbackData.map(fb => fb.sentiment),
        type: 'histogram',
    };

    Plotly.newPlot('sentimentChart', [sentimentData], {
        title: 'Sentiment Distribution',
        xaxis: { title: 'Sentiment' },
        yaxis: { title: 'Count' },
    });

    const featuresData = {
        x: feedbackData.filter(fb => fb.requested_feature).map(fb => fb.requested_feature),
        type: 'histogram',
    };

    Plotly.newPlot('featuresChart', [featuresData], {
        title: 'Requested Features',
        xaxis: { title: 'Feature' },
        yaxis: { title: 'Count' },
    });
});

// Função para gerar páginas da tabela
function generateTablePage(page) {
    const start = (page - 1) * recordsPerPage;
    const end = start + recordsPerPage;
    const tableBody = document.getElementById('feedbackTableBody');
    tableBody.innerHTML = '';

    for (let i = start; i < end && i < feedbackData.length; i++) {
        const statusClass = feedbackData[i].status;
        const statusTitle = statusClass === 'green' ? 'Feedback analisado' : 'Feedback ainda não analisado';
        const row = `<tr>
                        <td class="text-center align-middle">
                            <a href="#" class="btn custom-btn btn-sm" data-toggle="modal" data-target="#feedbackModal" data-feedback-id="${feedbackData[i].feedback_id}" title="Ver detalhes">
                                Mais detalhes
                            </a>
                        </td>
                        <td>${feedbackData[i].feedback_id}</td>
                        <td>${feedbackData[i].feedback}</td>
                        <td class="text-center align-middle">
                            <span class="status-circle ${statusClass}" title="${statusTitle}"></span>
                        </td>
                     </tr>`;
        tableBody.innerHTML += row;
    }
}

function generatePagination() {
    const totalPages = Math.ceil(feedbackData.length / recordsPerPage);
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const pageItem = `<li class="page-item ${i === currentPage ? 'active' : ''}">
                            <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
                          </li>`;
        pagination.innerHTML += pageItem;
    }
}

function changePage(page) {
    if (page < 1 || page > Math.ceil(feedbackData.length / recordsPerPage)) return;
    currentPage = page;
    generateTablePage(page);
    generatePagination();
}
