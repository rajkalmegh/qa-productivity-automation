
async function uploadFile(){

let file = document.getElementById("fileInput").files[0]

let formData = new FormData()

formData.append("file", file)

let response = await fetch("/generate-report", {
    method: "POST",
    body: formData
})

let data = await response.json()

document.getElementById("result").innerText =
"Report Generated in " + data.execution_time_seconds + " seconds"

}
