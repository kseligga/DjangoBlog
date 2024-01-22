
    var buttons = document.querySelectorAll('button');

    var blocks = document.querySelectorAll('.block1, .block2, .block3, .block4, .block5');

    for (let i = 1; i < blocks.length; i++) {
        blocks[i].style.display = 'none';
    }

    buttons.forEach((button, index) => {
        button.addEventListener('click', function() {
            for (let i = 0; i < blocks.length; i++) {
                blocks[i].style.display = 'none';
            }
            blocks[index].style.display = 'block';
        });
    });
