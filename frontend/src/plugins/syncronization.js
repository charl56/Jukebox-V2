import api from "./api"

export function SyncronizeCdWithBack() {

    // Creation du json qui sera save dans le fichier
    let data = {
        "cd": JSON.parse(localStorage.dataList)
    }
    // Requete vers le back pour save les données du JSON
    api.postApi("cd", { data: JSON.stringify(data) })
        .catch((err) => {
            console.log(err)
        })
}