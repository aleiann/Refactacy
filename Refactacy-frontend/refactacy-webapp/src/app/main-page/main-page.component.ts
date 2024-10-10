import { Component } from '@angular/core';
import { FileSelectionService } from '../file-selection.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css']
})
export class MainPageComponent {

  constructor(private fileSelectionService: FileSelectionService, private router: Router) {}

  selectedFileName: string = 'No file selected';
  selectedLanguage: string = 'Java';
  description: string = '';
  codeContent: string = 'No code';
  JavaCodeContent: string = '';

  async copyCodeCbl() {
    // Crea un elemento di input temporaneo per copiare il testo
    const textarea = document.createElement('textarea');
    textarea.value = this.codeContent;  // Imposta il contenuto del codice da copiare
    document.body.appendChild(textarea);
    textarea.select();  // Seleziona il testo
    document.execCommand('copy');  // Copia il testo negli appunti
    document.body.removeChild(textarea);  // Rimuove l'elemento temporaneo
    alert('Codice copiato negli appunti!');

  }

  async copyCodeJava() {
    // Crea un elemento di input temporaneo per copiare il testo
    const textarea = document.createElement('textarea');
    textarea.value = this.JavaCodeContent;  // Imposta il contenuto del codice da copiare
    document.body.appendChild(textarea);
    textarea.select();  // Seleziona il testo
    document.execCommand('copy');  // Copia il testo negli appunti
    document.body.removeChild(textarea);  // Rimuove l'elemento temporaneo
    alert('Codice copiato negli appunti!');

  }

  goToDoc() {
    this.router.navigate(['/doc']);
    const sidebar = document.getElementById('sidebar');
    if(sidebar){
      sidebar.style.display = 'none';
    }
  }
  
  // Funzione che aggiorna il nome del file selezionato
  ngOnInit() {
    this.fileSelectionService.selectedFile$.subscribe((fileName) => {
      if (fileName) {
        this.selectedFileName = fileName; // Aggiorna il file selezionato
      }
    });
    this.fileSelectionService.contentFile$.subscribe((fileContent) => {
      if (fileContent) {
        this.codeContent = fileContent; // Aggiorna il file selezionato
      }
    });
    this.fileSelectionService.contentJavaFile$.subscribe((fileContent) => {
      if (fileContent) {
        this.JavaCodeContent = fileContent; // Aggiorna il file selezionato
      }
    });
    this.fileSelectionService.descFile$.subscribe((fileDesc) => {
      if (fileDesc) {
        this.description = fileDesc; // Aggiorna il file selezionato
      }
    });
  }
}
