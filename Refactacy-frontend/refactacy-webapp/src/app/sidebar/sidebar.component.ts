import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FileSelectionService } from '../file-selection.service';
import { HttpClient, HttpParams } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';
import { OpenAIService } from '../openai.service';  // Assicurati di avere il percorso corretto
import extensionsData from '../../assets/extensions.json'; // Percorso del tuo file JSON
import { JavaCodeClass } from '../responseTranslationDto';

interface JavaASTResponse {
  javaCode: string;
}

interface getJavaCodePayload {
  owner: string;
  repo: string;
  path: string;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})

export class SidebarComponent implements OnInit {

  constructor(private http: HttpClient, private fileSelectionService: FileSelectionService, private openAIService: OpenAIService) { }
  response: any;
  private extensions = (extensionsData as any).extensions;
  sendName(name: string): void {
    this.openAIService.getName(name).subscribe(
      (data) => {
        this.response = data;  // Salva la risposta
        console.log('Risposta dal server:', data);
      },
      (error) => {
        console.error('Errore nella chiamata GET:', error);
      }
    );
  }

  private apiUrl = 'http://127.0.0.1:5000/getJavaCode'; // Indirizzo del servizio

  // Metodo per inviare il payload al servizio
  sendJavaCode(payload: any): Promise<JavaASTResponse | undefined> {
    return this.http.post<JavaASTResponse>(this.apiUrl, payload).toPromise();
  }
  // Metodo per inviare il payload al servizio
  getJavaCode(payload: any): Promise<string | undefined> {
    return this.http.post(this.apiUrl, payload, { responseType: 'text' }).toPromise();
  }

  wait(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async selectFile(item: any) {
    const animation = document.getElementById("translateAnimation");
    const buttonDocJava = document.getElementById('button-doc-java');
    const buttonDocCobol = document.getElementById('button-doc-cbl');
    const exampleJavaCodeObject = new JavaCodeClass(
      "import java.util.Scanner;\n\npublic class MainProgram {\n    // Variabili di lavoro\n    private static String wsUserChoice;\n    private static String wsAccountNumber;\n    private static double wsTransactionAmount;\n    private static double wsNewBalance;\n    private static CommArea commArea = new CommArea();\n\n    public static void main(String[] args) {\n        Scanner scanner = new Scanner(System.in);\n        System.out.println(\"Benvenuto nel sistema bancario!\");\n        System.out.println(\"1. Consulta il saldo\");\n        System.out.println(\"2. Esegui una transazione (deposito/prelievo)\");\n        System.out.println(\"Scegli l'operazione (1 o 2):\");\n        wsUserChoice = scanner.nextLine();\n\n        if (wsUserChoice.equals(\"1\")) {\n            consultaSaldo(scanner);\n        } else if (wsUserChoice.equals(\"2\")) {\n            transazione(scanner);\n        } else {\n            System.out.println(\"Scelta non valida\");\n        }\n        scanner.close();\n    }\n\n    // Funzione per consultare il saldo\n    private static void consultaSaldo(Scanner scanner) {\n        System.out.println(\"Inserisci il numero del conto:\");\n        wsAccountNumber = scanner.nextLine();\n        commArea.setAccountNumber(wsAccountNumber);\n        BalanceModule.call(commArea);\n        System.out.println(\"Il saldo corrente del conto \" + wsAccountNumber + \" è: \" + commArea.getNewBalance());\n    }\n\n    // Funzione per eseguire una transazione\n    private static void transazione(Scanner scanner) {\n        System.out.println(\"Inserisci il numero del conto:\");\n        wsAccountNumber = scanner.nextLine();\n        System.out.println(\"Inserisci l'importo della transazione (positivo per depositi, negativo per prelievi):\");\n        wsTransactionAmount = scanner.nextDouble();\n        commArea.setAccountNumber(wsAccountNumber);\n        commArea.setTransactionAmount(wsTransactionAmount);\n        TransactionModule.call(commArea);\n        System.out.println(\"Il saldo aggiornato del conto \" + wsAccountNumber + \" è: \" + commArea.getNewBalance());\n    }\n\n    // Classe per la comunicazione tra moduli\n    private static class CommArea {\n        private String accountNumber;\n        private double transactionAmount;\n        private double newBalance;\n\n        public String getAccountNumber() { return accountNumber; }\n        public void setAccountNumber(String accountNumber) { this.accountNumber = accountNumber; }\n\n        public double getTransactionAmount() { return transactionAmount; }\n        public void setTransactionAmount(double transactionAmount) { this.transactionAmount = transactionAmount; }\n\n        public double getNewBalance() { return newBalance; }\n        public void setNewBalance(double newBalance) { this.newBalance = newBalance; }\n    }\n\n    // Classe fittizia per il modulo saldo\n    private static class BalanceModule {\n        public static void call(CommArea commArea) {\n            // Implementazione fittizia per ottenere il saldo\n            commArea.setNewBalance(1000.0); // Simulazione del saldo\n        }\n    }\n\n    // Classe fittizia per il modulo transazione\n    private static class TransactionModule {\n        public static void call(CommArea commArea) {\n            // Implementazione fittizia per aggiornare il saldo\n            commArea.setNewBalance(commArea.getTransactionAmount() + 1000.0); // Simulazione del nuovo saldo\n        }\n    }\n}\n",
      "Il codice Java traduce il programma COBOL per un sistema bancario. Viene utilizzato Scanner per l'input utente e classi fittizie per simulare i moduli di saldo e transazione.",
      [
        { nameFunction: 'main', descriptionFunction: "La funzione main è il punto d'ingresso del programma. Prende input dall'utente per scegliere tra consultare il saldo o eseguire una transazione. In base alla scelta dell'utente, chiama la funzione appropriata." },
        { nameFunction: 'consultaSaldo', descriptionFunction: "La funzione consultaSaldo prende un oggetto Scanner come input per leggere il numero del conto dall'utente. Simula una chiamata al modulo del saldo e visualizza il saldo corrente del conto utente. Non restituisce alcun valore." },
        { nameFunction: 'transazione', descriptionFunction: "La funzione transazione prende un oggetto Scanner come input per leggere il numero del conto e l'importo della transazione dall'utente. Simula una chiamata al modulo della transazione e visualizza il saldo aggiornato del conto utente. Non restituisce alcun valore." },
        { nameFunction: 'CommArea', descriptionFunction: "La classe CommArea viene utilizzata per trasferire dati tra le funzioni e i moduli fittizi. Contiene i getter e setter per il numero del conto, l'importo della transazione e il nuovo saldo." },
        { nameFunction: 'BalanceModule', descriptionFunction: "La classe BalanceModule simula un modulo COBOL che restituisce il saldo corrente. La funzione call prende un oggetto CommArea come input e imposta il saldo corrente. Non restituisce alcun valore." },
        { nameFunction: 'TransactionModule', descriptionFunction: "La classe TransactionModule simula un modulo COBOL che aggiorna il saldo del conto. La funzione call prende un oggetto CommArea come input e aggiorna il saldo in base all'importo della transazione. Non restituisce alcun valore." }
      ]
    );

    if (item.type === 'file') {
      const javacode = document.getElementById("javaCode");
      if (buttonDocJava) {
        buttonDocJava.style.visibility = 'hidden';
      }
      if (buttonDocCobol) {
        buttonDocCobol.style.visibility = 'hidden';
      }
      if (javacode) {
        javacode.style.display = 'none';
      }
      if (animation) {
        animation.style.visibility = 'hidden';
      }
      const fileName = item.name;  // Estrai il nome del file
      this.fileSelectionService.selectFile(fileName); // Passa il nome del file al servizio
      this.getFileContent(item.path);  // Richiama il metodo per recuperare il contenuto del file
      const ext = this.getFileDesc(fileName);
      // Cerca l'estensione nel JSON
      const match = this.extensions.find((item: any) => item.extension === `.${ext}`);
      // Restituisce la descrizione se trovata, altrimenti un messaggio di errore
      const desc = match ? match.description : `Description for .${ext} not found.`;
      this.fileSelectionService.descFile(desc);
      console.log(ext);
      await this.wait(3000);
      if (ext == 'cbl') {
        if (buttonDocCobol) {
          buttonDocCobol.style.visibility = 'visible';
        }
        if (animation) {
          animation.style.visibility = 'visible';
        }
        const codeContent = await this.getFileContentWithoutModify(item.path);
        try {
          const result = await this.processFileContent(codeContent);
          const repository = {
            owner: this.owner,  // Sostituisci con il nome dell'owner
            repo: this.repo,     // Sostituisci con il nome del repository
            path: item.path      // Sostituisci con il percorso del file
          };
          const res = await this.getJavaCode(repository);

          if (res) {
            try {
              const javaCode = res;
              //const javaCode = exampleJavaCodeObject.javaCode;
              this.fileSelectionService.contentJavaFile(javaCode);
              if (animation) {
                animation.style.visibility = 'hidden';
              }
              if (javacode) {
                javacode.style.display = 'block';
              }
              if (buttonDocJava) {
                buttonDocJava.style.visibility = 'visible';
              }
            } catch (error) {
              console.error("Errore nel parsing della risposta:", error);
            }
          } else {
            console.error("Nessun risultato ricevuto.");
          }

        } catch (error) {
          console.error('Errore durante l\'elaborazione:', error);
        }
      } else {
        if (animation) {
          animation.style.visibility = 'hidden';
        }
        if (buttonDocJava) {
          buttonDocJava.style.visibility = 'hidden';
        }
        if (buttonDocCobol) {
          buttonDocCobol.style.visibility = 'hidden';
        }
        //this.sendName(fileName);
      }
    }

  }

  async processFileContent(fileContent: string): Promise<any> {
    // Regular expression per trovare le righe che iniziano con COPY "FILE.CPY"
    const regex = /^\s*COPY\s+"([A-Z0-9._-]+)\.CPY"/gm;
    let match;

    interface FileCpy {
      nome: string,
      contenuto: string
    }

    let jsonData: { fileCobol: string; filesCpy: FileCpy[] } = {
      fileCobol: fileContent,
      filesCpy: []
    };

    // Itera su tutte le occorrenze nella stringa
    while ((match = regex.exec(fileContent)) !== null) {
      // match[1] contiene la parte "FILE.CPY"
      let fileName = match[1];

      // Attendi la risoluzione della promise per ottenere il contenuto del file
      let fileContentCpy = await this.getFileContentWithoutModify(fileName + '.cpy');
      console.log('1caso:' + fileName);

      // Gestisci il caso in cui il file non venga trovato e tenti altre varianti
      if (fileContentCpy == '') {
        const camelCaseFileName = fileName.charAt(0).toUpperCase() + fileName.slice(1).toLowerCase();
        fileContentCpy = await this.getFileContentWithoutModify(camelCaseFileName + '.cpy');
        console.log('1caso:' + camelCaseFileName);
        if (fileContentCpy == '') {
          fileContentCpy = await this.getFileContentWithoutModify(fileName.toLowerCase() + '.cpy');
          console.log('1caso:' + fileName.toLowerCase());
        }
      }

      // Crea un nuovo oggetto di tipo FileCpy con il nome e il contenuto del file
      let newFile: FileCpy = {
        nome: fileName,
        contenuto: fileContentCpy
      };

      // Aggiungi il nuovo file alla lista filesCpy
      jsonData.filesCpy.push(newFile);
    }
    return jsonData;
  }


  repoUrl: string = '';
  contents: any[] = [];
  owner: string = '';
  repo: string = '';
  pathStack: string[] = [];  // Stack dei percorsi per la navigazione

  // Carica il contenuto della root del repository
  loadRepo() {
    const urlParts = this.repoUrl.split('/');
    this.owner = urlParts[urlParts.length - 2];
    this.repo = urlParts[urlParts.length - 1];
    this.fileSelectionService.repoName(this.owner + '/' + this.repo);
    console.log(this.repo);

    this.pathStack = []; // Reset dello stack quando si carica un nuovo repo

    this.http.get(`https://api.github.com/repos/${this.owner}/${this.repo}/contents`).subscribe(
      (data: any) => this.contents = data,
      (error) => console.error('Errore:', error)
    );
  }

  getFileDesc(name: string) {
    // Check if the filename contains a period and return the extension
    const extension = name.split('.').pop();

    // If no period or the string is empty after the last period, return an empty string
    return (extension === name) ? '' : extension;
  }

  // Carica il contenuto di una cartella
  loadFolder(path: string) {
    console.log('Aprendo la cartella:', path);

    // Aggiungi il percorso corrente allo stack
    this.pathStack.push(path);

    this.http.get(`https://api.github.com/repos/${this.owner}/${this.repo}/contents/${path}`).subscribe(
      (data: any) => this.contents = data,
      (error) => console.error('Errore:', error)
    );
  }

  // Funzione per navigare indietro
  goBack() {
    if (this.pathStack.length > 0) {
      this.pathStack.pop();  // Rimuovi l'ultimo percorso dallo stack

      // Ottieni il percorso precedente dallo stack o root se lo stack è vuoto
      const previousPath = this.pathStack.length > 0 ? this.pathStack[this.pathStack.length - 1] : '';

      this.http.get(`https://api.github.com/repos/${this.owner}/${this.repo}/contents/${previousPath}`).subscribe(
        (data: any) => this.contents = data,
        (error) => console.error('Errore:', error)
      );
    }
  }



  getFileContentWithoutModify(path: string): Promise<string> {

    // URL dell'API GitHub per ottenere il contenuto del file
    const url = `https://api.github.com/repos/${this.owner}/${this.repo}/contents/${path}`;

    // Restituiamo una Promise che risolve il contenuto del file
    return new Promise((resolve, reject) => {
      this.http.get(url).subscribe(
        (response: any) => {
          if (response && response.content) {
            const fileContent = atob(response.content);  // Decodifica il contenuto da base64
            resolve(fileContent);  // Risolviamo la Promise con il contenuto decodificato
          } else {
            console.error('Nessun contenuto trovato per questo file.');
            resolve('');
          }
        },
        (error) => {
          console.error('Errore nel recupero del contenuto del file:', error);
          resolve('');
        }
      );
    });
  }


  getFileContent(path: string): void {

    // URL dell'API GitHub per ottenere il contenuto del file
    const url = `https://api.github.com/repos/${this.owner}/${this.repo}/contents/${path}`;
    var fileContent1 = '';

    // Effettua la richiesta HTTP
    this.http.get(url).subscribe(
      (response: any) => {
        if (response && response.content) {
          const fileContent = atob(response.content);  // Decodifica il contenuto da base64
          this.fileSelectionService.contentFile(fileContent); // Passa il nome del file al servizio
        } else {
          console.error('Nessun contenuto trovato per questo file.');
        }
      },
      (error) => {
        console.error('Errore nel recupero del contenuto del file:', error);
      }
    );

  }

  isModalVisible: boolean = false;

  // Funzione per aprire la modale
  openModal(): void {
    const codesection = document.getElementById('code-section');
    const codesection2 = document.getElementById('code-section-2');
    if (codesection && codesection2) {
      codesection.style.visibility = 'hidden';
      codesection2.style.visibility = 'hidden';
    }

    this.isModalVisible = true;  // Mostra la modale
  }

  // Funzione per chiudere la modale
  closeModal() {
    const codesection = document.getElementById('code-section');
    const codesection2 = document.getElementById('code-section-2');
    if (codesection) {
      codesection.style.visibility = 'visible';
    }
    if (codesection2) {
      codesection2.style.visibility = 'visible';
    }
    this.isModalVisible = false;
  }

  ngOnInit(): void { }
}
