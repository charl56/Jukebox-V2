import axios from "axios"

export function SyncronizeCdWithBack(backendPort) {
    if (import.meta.env.VITE_CUSTOM_MODE) {
        return 
    }

    // Creation du json qui sera save dans le fichier
    let data = {
        "cd": JSON.parse(localStorage.dataList)
    }
    // Requete vers le back pour save les données du JSON
    axios.post(backendPort + "syncData", { data: JSON.stringify(data) })
        .catch((err) => {
            console.log(err)
        })
}