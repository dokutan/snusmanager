import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddSnus } from './add-snus';

describe('AddSnus', () => {
  let component: AddSnus;
  let fixture: ComponentFixture<AddSnus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddSnus]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddSnus);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
