// Dashboard utilities

function filterAssets(query) {
    const q = query.toLowerCase().trim();  //  the search text
    const rows = document.querySelectorAll('.asset-row');  // all table rows
    const noRes = document.getElementById('no-results');    // the "no results" row
    if (!noRes) return;
    let found = 0;  // counter for how many rows are visible

    rows.forEach(row => {
        const match = !q || row.dataset.title.includes(q);
        row.style.display = match ? '' : 'none';
        if (match) found++;
    });

    noRes.style.display = (q && found === 0) ? '' : 'none';
}

function copyPortfolioLink(url, btn) {
    navigator.clipboard.writeText(url).then(() => {
        const original = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check-lg"></i> Copied!';
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-success');
        setTimeout(() => {
            btn.innerHTML = original;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-secondary');
        }, 2000);
    }).catch(function (err) {
        if (err) console.error('copyPortfolioLink: clipboard.writeText failed', err);
        try {
            var input = document.createElement('input');
            input.value = url;
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy');
            document.body.removeChild(input);
            var original = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check-lg"></i> Copied!';
            setTimeout(function () { btn.innerHTML = original; }, 2000);
        } catch (fallbackErr) {
            console.error('copyPortfolioLink: fallback copy failed', fallbackErr);
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });
});
