function getColumn (content, columnIndex, skipLines = 0) {
    const rows = content.split("\n")
    let out = []
    for (let i = skipLines; i < rows.length-1; i++) {
        out.push(rows[i].trim().split(/\s+/)[columnIndex])
    }
    return out
}
