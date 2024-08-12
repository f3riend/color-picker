var socket = io.connect('http://' + document.domain + ':' + location.port, {
    transports: ['websocket']
});


const copyContent = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      console.log(`Content copied to clipboard ${text}`)
    } catch (err) {
      console.error('Failed to copy: ', err)
    }
}


socket.on('update', function(msg) {
    var ul = document.getElementById('namesList');
    ul.innerHTML = ''; // Clear the list
    msg.colors.forEach(function(color) {
        var li = document.createElement('li');
        li.innerHTML = `<span>COLORS</span><span><ion-icon name="copy"></ion-icon>rgb(${color[0]})</span><hr><span><ion-icon name="copy"></ion-icon>${color[1]}</span>`;
        ul.appendChild(li);
    });

    var list = document.querySelectorAll("ion-icon");

    list.forEach((e, i) => {
        function onClick() {
            const nextNode = this.nextSibling;
    
            if (nextNode && nextNode.nodeType === Node.TEXT_NODE) {
                // Gelen text düğümünü al
                const textContent = nextNode.textContent.trim();
                console.log("Next text content:", textContent);
    
                copyContent(textContent);
    
                this.classList.add('clicked');
    
                // Görsel geri bildirimi 2 saniye sonra kaldır
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 1000);
            }
        }
    
        e.addEventListener("click", onClick);
    });

    

    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });

});
