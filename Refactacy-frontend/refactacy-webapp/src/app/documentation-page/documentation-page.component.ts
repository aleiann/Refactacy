import { Component, OnInit } from '@angular/core';
import { FileSelectionService } from '../file-selection.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

interface descResponse {
  descriptionCode: string;
  documentation: functions[];
}

interface functions {
  nameFunction: string;
  descriptionFunction: string;
}

@Component({
  selector: 'app-documentation-page',
  templateUrl: './documentation-page.component.html',
  styleUrls: ['./documentation-page.component.css']
})
export class DocumentationPageComponent implements OnInit {
  constructor(private http: HttpClient, private fileSelectionService: FileSelectionService, private router: Router) {}

  selectedFileName: string = 'No file selected';
  JavaCodeContent: string = '';
  description = '';

  codeLines: string[] = [];  // Righe del codice sorgente
  methods = [
    { nameFunction: 'public static void main', descriptionFunction: 'Descrizione di funzione1' },
    { nameFunction: 'private static void consultaSaldo', descriptionFunction: 'Descrizione di funzione2' },
    { nameFunction: 'private static void eseguiTransazione', descriptionFunction: 'Descrizione di funzione1' },
    { nameFunction: 'public double getBalance', descriptionFunction: 'Descrizione di funzione2' },
    { nameFunction: 'public double updateBalance', descriptionFunction: 'Descrizione di funzione1' }
    // Aggiungi altre funzioni qui
  ];

  functions = []

  highlightedMethodStart: number | null = null;  // Indice di inizio metodo evidenziato
  highlightedMethodEnd: number | null = null;    // Indice di fine metodo evidenziato
  clickedMethodIndex: number | null = null;      // Metodo selezionato al click
  hoveredMethodIndex: number | null = null;      // Metodo evidenziato al passaggio del mouse

  async ngOnInit(): Promise<void> {
    this.fileSelectionService.contentJavaFile$.subscribe((fileContent) => {
      if (fileContent) {
        this.JavaCodeContent = fileContent; // Aggiorna il file selezionato
      }
    });
    this.codeLines = this.extractCodeLines(this.JavaCodeContent);
    console.log(this.JavaCodeContent);
    if(this.JavaCodeContent != ''){
      const payload = {
        javaCode: this.JavaCodeContent
      }
      const res = await this.getDocumentation(payload);
      if(res){
        this.methods = res?.documentation;
        this.fileSelectionService.descFile(res.descriptionCode);
      }
    }
    this.fileSelectionService.descFile$.subscribe((desc) => {
      if (desc) {
        this.description = desc; // Aggiorna il file selezionato
      }
    });
    this.fileSelectionService.selectedFile$.subscribe((fileName) => {
      if (fileName) {
        this.selectedFileName = fileName; // Aggiorna il file selezionato
      }
    });
  }

  private apiUrl = 'http://127.0.0.1:5000/getDoc'; // Indirizzo del servizio
  

  // Metodo per inviare il payload al servizio
  getDocumentation(payload: any): Promise<descResponse | undefined> {
    return this.http.post<descResponse>(this.apiUrl, payload).toPromise();
  }

  // Funzione per evidenziare il metodo al passaggio del mouse
  onMouseEnterMethod(index: number): void {
    const range = this.findMethodRangeForLine(index);
    if (range) {
      this.highlightedMethodStart = range.start;
      this.highlightedMethodEnd = range.end;

      // Trova l'indice del metodo corrispondente per mostrare nome e descrizione
      this.hoveredMethodIndex = this.methods.findIndex(method => 
        this.codeLines[range.start].includes(method.nameFunction)
      );
    }
  }

  // Funzione per selezionare un metodo con il click
  onMethodClick(index: number): void {
    this.clickedMethodIndex = this.hoveredMethodIndex;  // Mantiene il metodo selezionato fino a un altro click
  }

  // Funzione per rimuovere l'evidenziazione del metodo al mouseleave
  onMouseLeaveMethod(): void {
    if (this.clickedMethodIndex === null) {
      this.highlightedMethodStart = null;
      this.highlightedMethodEnd = null;
      this.hoveredMethodIndex = null;  // Solo se non c'è un metodo selezionato al click
    }
  }

  // Funzione per verificare se una riga fa parte del metodo evidenziato o selezionato
  isLineInHighlightedMethod(index: number): boolean {
    return (this.highlightedMethodStart !== null &&
           this.highlightedMethodEnd !== null &&
           index >= this.highlightedMethodStart &&
           index <= this.highlightedMethodEnd);
  }

  // Trova l'intervallo (start, end) di righe del metodo corrispondente
  findMethodRangeForLine(lineIndex: number): { start: number; end: number } | null {
    for (let i = 0; i < this.methods.length; i++) {
      const methodSignature = this.methods[i].nameFunction; // Firma del metodo

      if (this.codeLines[lineIndex].includes(methodSignature)) {
        const start = lineIndex;
        const end = this.findMethodEnd(start);
        return { start, end };
      }
    }
    return null;
  }

  // Trova la fine del metodo (indice della prima parentesi graffa chiusa `}`)
  findMethodEnd(startIndex: number): number {
    let openBraces = 0;
    for (let i = startIndex; i < this.codeLines.length; i++) {
      if (this.codeLines[i].includes('{')) {
        openBraces++;
      }
      if (this.codeLines[i].includes('}')) {
        openBraces--;
      }
      if (openBraces === 0) {
        return i; // La fine del metodo è alla chiusura dell'ultima parentesi graffa
      }
    }
    return startIndex; // Se non trova la chiusura, ritorna lo stesso inizio
  }

  getCode(): string{
    let code = "";
    this.codeLines.forEach(line => {
      code += "\n" + line;
    });
    console.log(code);
    return code;
  }

  async copyCode() {
    // Crea un elemento di input temporaneo per copiare il testo
    const textarea = document.createElement('textarea');
    textarea.value = this.getCode();  // Imposta il contenuto del codice da copiare
    document.body.appendChild(textarea);
    textarea.select();  // Seleziona il testo
    document.execCommand('copy');  // Copia il testo negli appunti
    document.body.removeChild(textarea);  // Rimuove l'elemento temporaneo
    alert('Codice copiato negli appunti!');

  }

  // Funzione per estrarre il codice come array di stringhe
  extractCodeLines(code:string): string[] {
    return code.split('\n');
    /*return `
      public void funzione1() {
        // Corpo della funzione 1
        int x = 10;
        if (x > 0) {
          // condizione
        }
      }

      public void funzione2() {
        // Corpo della funzione 2
        for (int i = 0; i < 10; i++) {
          // ciclo
        }
        funzione1();
      }
    `.split('\n'); // Dividi il codice in righe*/
  }
}
