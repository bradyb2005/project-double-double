const PLATES = ['rings', 'rays', 'grid', 'bars', 'dots', 'waves']
export const plateFor = (n) => PLATES[Math.abs(Number(n) || 0) % PLATES.length]
