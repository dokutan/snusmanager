import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditSnus } from './edit-snus';

describe('EditSnus', () => {
  let component: EditSnus;
  let fixture: ComponentFixture<EditSnus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditSnus]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditSnus);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
