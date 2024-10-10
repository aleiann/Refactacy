import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FileSelectionService {
  // La variabile "globale" che conterrà il nome del file selezionato
  private selectedFileSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  selectedFile$ = this.selectedFileSubject.asObservable();

  // La variabile "globale" che conterrà il nome del file selezionato
  private contentFileSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  contentFile$ = this.contentFileSubject.asObservable();

  // La variabile "globale" che conterrà il nome del file selezionato
  private contentJavaFileSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  contentJavaFile$ = this.contentJavaFileSubject.asObservable();

  // La variabile "globale" che conterrà il nome del file selezionato
  private descFileSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  descFile$ = this.descFileSubject.asObservable();

  // La variabile "globale" che conterrà il nome del file selezionato
  private contentCpyFileSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  contentCpyFile$ = this.contentCpyFileSubject.asObservable();

  // La variabile "globale" che conterrà il nome del file selezionato
  private repoNameSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  repoName$ = this.repoNameSubject.asObservable();


  // Metodo per aggiornare il file selezionato
  selectFile(fileName: string) {
    this.selectedFileSubject.next(fileName); // Aggiorna il nome del file selezionato
  }

  contentFile(fileContent: string) {
    this.contentFileSubject.next(fileContent); // Aggiorna il nome del file selezionato
  }

  contentJavaFile(fileContent: string | void) {
    if (fileContent) {
      this.contentJavaFileSubject.next(fileContent); // Aggiorna il contenuto del file selezionato
    } else {
      this.contentJavaFileSubject.next(null); // Passa null se fileContent è void
    }  }

  contentCpyFile(fileContent: string) {
    this.contentCpyFileSubject.next(fileContent); // Aggiorna il nome del file selezionato
  }

  descFile(fileDesc: string) {
    this.descFileSubject.next(fileDesc); // Aggiorna il nome del file selezionato
  }

  repoName(repoName: string) {
    this.repoNameSubject.next(repoName); // Aggiorna il nome del file selezionato
  }
}
