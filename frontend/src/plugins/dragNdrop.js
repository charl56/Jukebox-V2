let acutalDrag

// Permet d'afficher un icon quand l'album peut être laché
export function allowDrop(ev) {
    ev.preventDefault();
}
// Permet de savoir quel cd est pris en drag
export function drag(album) {
    acutalDrag = album
}
// Recupère le cd drag
export function drop() {
    return acutalDrag
}