document.addEventListener('DOMContentLoaded', function() {
    const knowledgeBaseLink = document.querySelector('#knowledgeBaseLink');
    const topicsContainer = document.querySelector('#topicsContainer');

    knowledgeBaseLink.addEventListener('click', function() {
        fetch('/tickets/themes/')
            .then(response => response.json())
            .then(data => {
                topicsContainer.innerHTML = '';
                data.forEach(topic => {
                    const topicItem = document.createElement('li');
                    const topicLink = document.createElement('a');
                    topicLink.href = `/tickets/knowledges?id=${topic.id}`;
                    topicLink.textContent = topic.name;

                    topicItem.appendChild(topicLink);
                    topicsContainer.appendChild(topicItem);
                });
                topicsContainer.classList.toggle('d-none');
            });
    });
});
