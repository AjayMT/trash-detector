
let submitButton = document.getElementById('submit')

submitButton.addEventListener('click', () => {
  let image = document.getElementById('input_image')
  if (image.files.length === 0) {
    alert('Please upload a file')
    return
  }

  document.getElementById('result-span').innerHTML = 'Loading...'

  let fd = new FormData()
  fd.append('input_image', image.files[0])

  BlobBuilder = window.MozBlobBuilder || window.WebKitBlobBuilder || window.BlobBuilder;

  let request = new XMLHttpRequest();
  request.open('POST', '/', true);
  request.responseType = 'blob';
  request.onreadystatechange = () => {
    if (request.status === 200) {
      let urlCreator = window.URL || window.webkitURL
      let imageURL = urlCreator.createObjectURL(request.response)
      document.getElementById('result-span').innerHTML = ''
      document.getElementById('result').src = imageURL
    }
  }
  request.send(fd);
})
