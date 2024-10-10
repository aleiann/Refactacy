import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DocumentationService {
  // La variabile "globale" che conterrà il nome del file selezionato
  private selectedFileSubject = new BehaviorSubject<string | null>(null);
  
  // Observable al quale i componenti possono iscriversi
  selectedFile$ = this.selectedFileSubject.asObservable();

  // Metodo per aggiornare il file selezionato
  selectFile(fileName: string) {
    this.selectedFileSubject.next(fileName); // Aggiorna il nome del file selezionato
  }
 
}
