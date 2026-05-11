export function extractChaupaiIndices(gridIndex, totalCells = 324, jump = 12, count = 9) {
  return Array.from({ length: count }, (_, step) => (gridIndex + step * jump) % totalCells);
}

export function extractChaupai(gridIndex, matrix, totalCells = 324, jump = 12, count = 9) {
  const indices = extractChaupaiIndices(gridIndex, totalCells, jump, count);
  return indices.map((index) => matrix[index] || "").join("");
}
