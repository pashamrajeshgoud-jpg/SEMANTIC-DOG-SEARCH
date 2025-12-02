import React, { useState } from 'react';

export default function App() {
    const [q, setQ] = useState('');
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [selected, setSelected] = useState(null);

    async function onSearch(e) {
        e && e.preventDefault();
        if (!q.trim()) return;
        setLoading(true);
        setError(null);
        setResults(null);
        try {
            const res = await fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(q)}`);
            if (!res.ok) throw new Error('No Results Found');
            const data = await res.json();
            setResults(data);
        } catch (err) {
            setError(err.message);
        } finally { setLoading(false); }
    }

    return (
        <div className="app">
            <header>
                <h1>Dog Search</h1>
                <p className="lead">Search by name or description (e.g. “small friendly dogs”)</p>
            </header>

            <form onSubmit={onSearch} className="search">
                <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search dog breeds or describe what you want..." />
                <button type="submit">Search</button>
            </form>

            {loading && <p>Loading…</p>}
            {error && <p className="error">{error}</p>}

            {results && (
                <div className="grid">
                    {results.map(r => (
                        <div key={r.id} className="card" onClick={() => {
                            setSelected(r);
                        }}>
                            {r.image ? <img src={r.image} alt={r.name} /> : <div className="placeholder">No image</div>}
                            <div className="meta">
                                <h3>{r.name}</h3>
                                <p><strong>Temperament:</strong> {r.temperament || '—'}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Modal for selected breed */}
            {selected && (
                <div className="modal" onClick={() => setSelected(null)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <button className="close" onClick={() => setSelected(null)}>×</button>
                        <h2>{selected.name}</h2>
                        {selected.image ? <img src={selected.image} alt={selected.name} /> : <div className="placeholder">No image</div>}
                        <p><strong>Temperament:</strong> {selected.temperament || '—'}</p>
                        <p><strong>Description:</strong> {selected.description || '—'}</p>
                        <p><strong>Life Span:</strong> {selected.life_span || '—'}</p>
                        <p><strong>Bred For:</strong> {selected.bred_for || '—'}</p>
                    </div>
                </div>
            )}
        </div>
    );
}
