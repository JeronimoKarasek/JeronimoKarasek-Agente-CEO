document.addEventListener('DOMContentLoaded', () => {

    try {
        lucide.createIcons();
    } catch (error) {
        console.error("Lucide icons could not be created.", error);
    }


    const copyButtons = document.querySelectorAll('.copy-btn');

    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const wrapper = button.closest('.code-block-wrapper');
            if (!wrapper) return;

            const codeElement = wrapper.querySelector('code');
            if (!codeElement) return;

            const codeToCopy = codeElement.innerText;

            navigator.clipboard.writeText(codeToCopy).then(() => {
                const buttonText = button.querySelector('span');
                const buttonIcon = button.querySelector('i');

                const originalText = buttonText.textContent;
                const originalIcon = buttonIcon.getAttribute('data-lucide');
                
                buttonText.textContent = 'Copied!';
                button.classList.add('copied');
                
                if (buttonIcon) {
                    buttonIcon.setAttribute('data-lucide', 'check');
                    lucide.createIcons();
                }

                setTimeout(() => {
                    buttonText.textContent = originalText;
                    button.classList.remove('copied');
                    if (buttonIcon) {
                        buttonIcon.setAttribute('data-lucide', originalIcon);
                        lucide.createIcons();
                    }
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                const buttonText = button.querySelector('span');
                buttonText.textContent = 'Error';
                setTimeout(() => {
                     buttonText.textContent = 'Copy';
                }, 2000);
            });
        });
    });
});
