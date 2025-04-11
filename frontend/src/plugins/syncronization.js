import api from "./api"
import { eventBus } from "./eventBus"

export function SyncronizeCdWithBack() {

    // Creation du json qui sera save dans le fichier
    let data = {
        "cd": JSON.parse(localStorage.dataList)
    }
    // Requete vers le back pour save les données du JSON
    api.postApi("cd", { data: JSON.stringify(data) })
        .then((res) => {
            if (res.status === "info") {
                eventBus.emit('showToast', {
                    title: "Message d'information",
                    content: res.message
                });
            }
        })
        .catch((err) => {
            console.log(err)
        })
}