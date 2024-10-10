import { Component, OnInit } from '@angular/core';
import { FileSelectionService } from '../file-selection.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(private fileSelectionService: FileSelectionService, private router: Router) { }
  repoName:string = 'No repo Connected';

  goToCtJ(){
    this.router.navigate(['/main']);
    const sidebar = document.getElementById('sidebar');
    if(sidebar){
      sidebar.style.display = 'block';
    }
  }

  goToDoc(){
    this.router.navigate(['/doc']);
    const sidebar = document.getElementById('sidebar');
    if(sidebar){
      sidebar.style.display = 'none';
    }
  }

  ngOnInit(): void {
    this.fileSelectionService.repoName$.subscribe((name) => {
      if (name) {
        this.repoName = name; // Aggiorna il file selezionato
      }
    });
  }

}
