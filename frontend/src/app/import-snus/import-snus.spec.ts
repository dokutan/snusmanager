import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImportSnus } from './import-snus';

describe('ImportSnus', () => {
  let component: ImportSnus;
  let fixture: ComponentFixture<ImportSnus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImportSnus]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImportSnus);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
