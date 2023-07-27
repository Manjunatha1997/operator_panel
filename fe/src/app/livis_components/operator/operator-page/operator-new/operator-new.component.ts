import { StorageService } from '../../../../helpers/storage.service';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import swal from 'sweetalert2';
import { ShiftService } from '../../../../services/shift.service';
import { AlertService } from '../../../../services/alert.service';
import { AuthenticationService } from '../../../../services/authentication.service';
// import { PlanningService } from 'src/app/services/planning.service';
import { PmodelService } from 'src/app/services/pmodel.service';
import { OperatorService } from 'src/app/services/operator.service';
import {ChangeDetectorRef } from '@angular/core';
import { MarutiOperatorService } from 'src/app/services/maruti-operator.service';
import {livisConfig} from "../../../../../config/constants";
import { identifierModuleUrl } from '@angular/compiler';

const demo_config = livisConfig['demo_config'];

// import {ToyodaPartService} from "../../../services/toyoda-part.service";

declare const $: any;
@Component({
  selector: 'app-operator-new',
  templateUrl: './operator-new.component.html',
  styleUrls: ['./operator-new.component.css']
})
export class OperatorNewComponent implements OnInit {
  user_info: any;
  camera_urls: any = [];
  loginForm: FormGroup;
  inspectionQcForm: FormGroup;
  pdnCounterForm: FormGroup;
  processStartForm: FormGroup;
  rescanForm: FormGroup;
  isSubmitted = false;
  part_list = [];
  current_process: any = {};
  metrix_list: any = {};

  defect_list: any=[] ;
  current_inspection_id: any = null;
  defectListInterval: any;
  metrixListInterval: any;
  runningProcessInterval: any;

  border = [];
  process_summary: any = {};
  production_counter: any;
  inspection_count = 0;
  cancel_text: any = 'Cancel';
  planInfo: any;
  shiftInfo: any;
  partInfo: any;
  isEditing = false;

  sealentMin: number;
  editSealentMin = false;
  sealentMax: number;
  editSealentMax = false;
  flangeMin: number;
  editFlangeMin = false;
  flangeMax: number;
  editFlangeMax = false;
  breakageMin: number;
  editBreakageMin = false;
  breakageMax: number;
  editBreakageMax = false;
  masticSealentMin: number;
  editMasticSealentMin = false;
  masticSealentMax: number;
  editMasticSealentMax = false;

  dimensions = {
    sealentMin: 0,
    sealentMax: 0,
    flangeMin: 0,
    flangeMax: 0,
    breakageMin: 0,
    breakageMax: 0,
    masticSealentMin: 0,
    masticSealentMax: 0,
  };

  reached_status_alert = false;
  selected_part_item: any = "";
  isProcessRunning: boolean = false;
  ocr_status: any;
  burr_status: any;
  running_inspection_id: any = null;
  selectedPartName: any;
  total_count: any=null;
  total_accepted: any=null;
  total_rejected: any=null;
  border_ocr: any=[];
  overall_status: any;
  inspection_status: any='--';
  reasons: any;
  border_defect: [];
  dent_on_elastomer: any;
  dent_on_thermostat: any;
  saw_tooth_damage: any;
  thread_damage: any;
  printing_erase: any;
  nextSlideLength: any = 0;
  pageNumber: any = parseInt(localStorage.getItem('carousal-page-number'))/8+1;
  thermostat_printing_erase: any;
  elastomer_printing_erase: any;
  camera_list: any = [];
  acceptedCount: any;
  totalCount: any;
  rejectedCount: any;
  inspection_payload: any;
  partafterSelect: any;
  stud_count: any;

  

  constructor(
    private _fb: FormBuilder,
    private operatorService: OperatorService,
    private shiftService: ShiftService,
    // private planService: PlanningService,
    private partService: PmodelService,
    private authenticationService: AuthenticationService,
    private alertService: AlertService,
    private storageService: StorageService,
    private marutiService: OperatorService,
    private cdref: ChangeDetectorRef,

  ) { }

  ngOnInit(): void {
    this.user_info = this.storageService.getUserDetails();
    this.loadProcessStartForm()

    this.getPartList();

    this.getRunningProcess()
    this.cameraLayoutLoad();
    // this.getCameraFeedUrl()
    // for(let i=0;i<2;i++) {
    //   document.getElementById(`full-screen-icon-open-${i}`).addEventListener('click',this.goFullScreen.bind(this))
    // }
  }


  loadProcessStartForm() {
    this.processStartForm = this._fb.group({
      // workstation_id: ['', [Validators.required]],
      // operator_id: ['', [Validators.required]],
      part_name: ['', [Validators.required]],
      // part_id: ['', [Validators.required]],
    });
  }

  getPartList() {
    //////console.log("INSIDE GET ALL PARTS")
    this.marutiService.getAllParts().subscribe((data) => {
      this.part_list = data;
      //////console.log("GET ALL PARTS==============================>", this.part_list);
      
    });
  }

  getCameraFeedUrl() {
    //////console.log("INSIDE GCFU");
    this.operatorService
      .getCameraFeed()
      .subscribe((data) => {
        this.camera_urls = data.data;
        //////console.log(this.camera_urls)
        // this.cameraLayoutLoad();
        this.cameraLayoutLoad();
        // for(let i=0;i<2;i++) {
        //   document.getElementById(`full-screen-icon-open-${i}`).addEventListener('click',this.goFullScreen.bind(this))
        // }
      });
  }

  // cameraLayoutLoad()  {
  //   var html = ``;
    
  //   var count_div =4;
  //   var col_size = 6;
  //   this.camera_list =[];   
  //   var camera_list =[];   
  //   //  this.camera_list = demo_config.IMAGE_URL;

  //   //////console.log(this.camera_list)

  //   // this.getCameraUrl();

  //   for (var i = 0; i < count_div; i++) {
  //     if (camera_list[i]) {
  //       html += `<div style="position:relative !important;padding-right:5px;padding-left:5px; height:${
  //         count_div <= 2 ? '85vh' : '40vh'
  //       }" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
  //       <div  class="fullscreen-box" style="position:absolute !important; top: 30px; right: 50px;  z-index: 100 !important;" (click)="goFullScreen()" id="full-screen-icon-open-${i}">
  //         <span><img src="../../../../../assets/img/fullscreen.png" width= "35px" alt=""></span>
  //       </div>
        
  //       <div  class="live-box" style="position:absolute !important;bottom: 30px;left: 50px;z-index: 100 !important;">
  //               <span><img src="../../../../../assets/img/live.png"     width= "100%" alt=""></span>
  //       </div>
  //       <div  class="status-box" style="    position:absolute !important;top: 30px;left: 50px;z-index: 100 !important;">
  //             <div class="status-status-box" id="status-box-${i}" style="display: flex;justify-content: center; align-items: center;background-color: var(--livis-bg-color);color: var(--livis-color);box-shadow: 0 2px 2px 0 rgb(55 197 171 / 14%), 0 3px 1px -2px rgb(55 197 171 / 20%), 0 1px 5px 0 rgb(55 197 171 / 12%);border-radius: 12px;max-width: 100px !important;">`;
  //             if(this.inspection_status != '--'){

  //               for(let j = 0 ; j<this.inspection_status[i].length ; j++) {
  //                 if(this.inspection_status[i] == "Rejected"){
  //                   html += `<span   style="background: red !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Rejected</span>`
  //                 }else{
  //                   html += `<span   style="background: green !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Accepted</span>`
  //                 }
  //               }
  //             }
  //             `

  //             </div>
  //             <div  class="defect-under-status row" style="margin-top: 10px !important;background: none !important;color: white !important;">`;
  //             if(this.defect_list && this.defect_list.length > 0){

  //             for(let j = 0 ; j<this.defect_list[i].length ; j++) {
  //               html += `<span class=" col-md-12 col-md-12 status-defect" style="padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;"> ${this.defect_list[i][j]} </span>`
  //             }
  //           }
  //             html += ` </div> 
  //       </div>


  //       <img style="width:100%;height:100%" src="http://${
  //         // camera_list[i + this.nextSlideLength]
  //         camera_list[i]
  //       }" id="live_feed_${i + 1}" alt="feed not available" >
  //         </div>`;


  //     } else {
  //       html += `<div style="position:relative !important ;padding-right:5px;padding-left:5px; height:${
  //         count_div <= 2 ? '85vh' : '43vh'
  //       }" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" id="full-view-${i}" >
  //       <div  class="fullscreen-box" style="position:absolute !important; top: 30px; right: 50px;  z-index: 100 !important;" (click)="goFullScreen()" id="full-screen-icon-open-${i}">
  //         <span><img src="../../../../../assets/img/fullscreen.png" width= "35px" alt=""></span>
  //       </div>
        
        
  //       <div  class="live-box" style="position:absolute !important;bottom: 30px;left: 50px;z-index: 100 !important;">
  //               <span><img src="../../../../../assets/img/live.png"     width= "100%" alt=""></span>
  //       </div>
  //       <div  class="status-box" style="    position:absolute !important;top: 30px;left: 50px;z-index: 100 !important;">
  //             <div class="status-status-box" id="status-box-${i}" style="display: flex;justify-content: center; align-items: center;background-color: var(--livis-bg-color);color: var(--livis-color);box-shadow: 0 2px 2px 0 rgb(55 197 171 / 14%), 0 3px 1px -2px rgb(55 197 171 / 20%), 0 1px 5px 0 rgb(55 197 171 / 12%);border-radius: 12px;max-width: 100px !important;">`;
  //             if(this.inspection_status != '--'){

  //               for(let j = 0 ; j<this.inspection_status[i].length ; j++) {
  //                 if(this.inspection_status[i] == "Rejected"){
  //                   html += `<span   style="background: red !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Rejected</span>`
  //                 }else{
  //                   html += `<span   style="background: green !important ; color:white !important;padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;">Accepted</span>`
  //                 }
  //               }
  //             }
  //             `</div>
  //             <div  class="defect-under-status row" style="margin-top: 10px !important;background: none !important;color: white !important;">`;
  //             if(this.defect_list && this.defect_list.length > 0){

  //               for(let j = 0 ; j<this.defect_list[i].length ; j++) {
  //                 html += `<span class=" col-md-12 col-md-12 status-defect" style="padding-inline: 25px ;padding-block: 10px ;border-radius: 12px;"> ${this.defect_list[i][j]} </span>`
  //               }
  //             }
  //               html += ` </div> 
  //       </div>

  //       <img style="width:100%;height:100%" src="../../../../assets/img/backpreview.png" id="live_feed_${
  //         i + 1
  //       }" alt="feed not available" >

  //         </div>`;
  //     }
  //   }
  //   $("#camera_layout_wrap").html(html);
  // }

  cameraLayoutLoad()  {
    var html = ``;
    
    var count_div =1;
    var col_size = 12;
    this.camera_list =[];   
    //  this.camera_list =this.camera_urls;
     this.camera_list = demo_config.IMAGE_URL;
    //////console.log(this.camera_list)

    // this.getCameraUrl();

    for(var i =0;i<count_div;i++)
    {
      if((this.camera_list[i])){
        html += `<div style="padding:5px !important" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:88vh; border-radius:30px !important" src="${this.camera_list[i]}" id="live_feed_${(i+1)}" alt="feed not available"  >
          </div>`;
      }else{
        html += `<div style="padding:5px !important; height:100%" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:88vh; border-radius:30px !important" src="../../../../../assets/img/backpreview.png" id="live_feed_${(i+1)}" alt="feed not available" >
          </div>`;
      }
    }
    $("#camera_layout_wrap").append(html);
  }


  getRunningProcess() {
    //////console.log("GET RUNNING PROCESS",     this.isProcessRunning )
    this.marutiService
      .getRunningProcess()
      .subscribe((data : any) => {
        if(data[0]==null){
          return
        }
        //////console.log(data[0]==null)
        this.isProcessRunning = true;
        this.current_process = data;
        this.running_inspection_id =  data[0]._id ;
        this.selectedPartName =this.processStartForm.value.part_name;

          this.partafterSelect =  data[0].part_name 
        // this.selectedPartName = data.part_name; //TODO: refer detzo_coil code
        //////console.log("RUNNING!!!", this.current_process);
        //////console.log("RUNNING!!!", this.running_inspection_id, this.partafterSelect);
        // if (Object.keys(data).length !== 0) {
          // if (this.running_inspection_id && this.isProcessRunning) {

            // if(this.isProcessRunning) {
              //////console.log("Yes")
              this.getMetrix();
              $('#start_process_btn').addClass('invisible');
              $('#stop_process_btn').removeClass('invisible');
              $('#inspect_btn').removeClass('invisible');
              // this.getCameraFeedUrl();
            // }

          // }
        // } else {

        // }
      }, );


  }


  showStartForm() {

  }
  partChange(value) {
    //////console.log(value)
    this.selected_part_item = value;


    this.processStartForm.patchValue({
      // operator_id: this.user_info.user_id,
      part_name: this.selected_part_item,
    });
    //////console.log("ON CHANGE",this.selected_part_item);
    this.cdref.detectChanges();
  }

  startProcess(model:any) {

    //////console.log("MODEL SEL", this.processStartForm);
    // //////console.log(this.user_info)
    this.isProcessRunning = true;
    if (this.processStartForm.value.part_name == ""){
      return 
    }
      let body = {
        // user_id: this.user_info._id,
        part_name:this.processStartForm.value.part_name,
      }
      this.marutiService.startProcess(body).subscribe((data) => {
        //////console.log("INSIDE STARTING")
        this.alertService.alertMessage(
          'Process Started Successfully',
          'success',
          'check'
        );
        this.current_process.inspection_id = data.current_inspection_id;
        this.selectedPartName = this.processStartForm.value.part_name;

        this.getRunningProcess();
        // this.getCameraFeedUrl();

        $('#start_process_btn').addClass('invisible');
        $('#stop_process_btn').removeClass('invisible');
    $('#inspect_btn').removeClass('invisible');

        $('#process-start-modal').modal('hide');
      }, error=> {
        //////console.log("NO SHIFT");
      });

  }

  processEndForm() {


    swal({
      title: '',
      text: 'Are you sure you want to end process',
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Ok',
      cancelButtonText: 'Cancel',
      confirmButtonClass: 'btn btn-success',
      cancelButtonClass: 'btn btn-danger',
      buttonsStyling: false,
    }).then((result) => {
      if (1) {
        if (result.value) {
          const end_info = { inspection_id: this.running_inspection_id };

          this.marutiService.endProcess(end_info).subscribe((response) => {
            $('#stop_process_btn').addClass('invisible');
            $('#inspect_btn').addClass('invisible');
            $('#start_process_btn').removeClass('invisible');
            $('#result-status-text').text('');
          //////console.log("INSIDE END!!!!!!!!!!!!!!!!!!!!!!!!!!", this.metrixListInterval);
          if (this.metrixListInterval) {
            clearTimeout(this.metrixListInterval);
          }
          this.inspection_status = "--";
      //////console.log(this.inspection_status)
      this.defect_list = [""]
      this.acceptedCount = 0
      this.rejectedCount = 0
      this.totalCount = 0
          this.selected_part_item = ""

          });
        }
      } else {
        this.quantityAlert();
      }
    });
  }


  quantityAlert() {
    swal({
      title: 'Quantity Alert',
      html:
        "<h4 class='text-danger'>Planned production not achieved.You cant end the process</h4>",
      buttonsStyling: false,
      confirmButtonClass: 'btn btn-danger',
      type: 'error',
    }).catch(swal.noop);
  }

  processEndedAlert() {
    this.current_process = {};
    this.partInfo = {};
    this.planInfo = {};
    this.shiftInfo = {};
    this.defect_list = [];
    this.metrix_list = {};

    if (this.runningProcessInterval) {
      clearTimeout(this.runningProcessInterval);
    }
    if (this.defectListInterval) {
      clearTimeout(this.defectListInterval);
    }
    if (this.metrixListInterval) {
      clearTimeout(this.metrixListInterval);
    }
    swal({
      title: '',
      html: "<h3 class='text-success'>Process Ended</h3>",
      buttonsStyling: false,
      confirmButtonClass: 'btn btn-success',
      type: 'success',
    }).catch(swal.noop);
  }


  endmetrix(){
    this.marutiService.getMetrix(this.running_inspection_id).subscribe((data : any) => {
      let result;  

      this.inspection_status = data.status;
      //////console.log(this.inspection_status)
      this.defect_list = data.defect_list
      this.acceptedCount = data.total_accepted
      this.rejectedCount = data.total_rejected
      this.totalCount = data.total
    });
  }


  getMetrix() {
    //////console.log("getmetrix")
    this.marutiService.getMetrix(this.running_inspection_id).subscribe((data : any) => {
      let result;  
      // this.selected_part_item = data.part_name
      // ////console.log(this.selected_part_item)
      // this.inspection_status = data.status;
      // //////console.log(this.inspection_status)
      // this.defect_list = data.defect_list
      // this.acceptedCount = data.total_accepted
      // this.rejectedCount = data.total_rejected
      // this.totalCount = data.total
      this.selected_part_item = data.part_name
      ////console.log(this.selected_part_item)
      this.inspection_status = data.status;
      this.stud_count = data.count
      //////console.log(this.inspection_status)
      this.defect_list = data.reject_reason.defects
      this.acceptedCount = data.total_accepted
      this.rejectedCount = data.total_rejected
      this.totalCount = data.total
    });
    this.isProcessRunning=true;
    this.metrixListInterval = setTimeout(() => {
      this.getMetrix();
    }, 1000);
  }


//   goFullScreen(i:any){
//     ////console.log(i.currentTarget.id[i.currentTarget.id.length-1])
//     ////console.log(i.currentTarget.id)
//     var elem = document.getElementById(`full-view-${i.currentTarget.id.substring(22,)}`);
    
//     if(elem.requestFullscreen){
//         elem.requestFullscreen();
//         $("#full-screen-icon-close").removeClass("invisible")
//         $("#full-screen-icon-open").addClass("invisible")
//     }
//     if(document.exitFullscreen){
      
//   $("#full-screen-icon-open").removeClass("invisible")
//   $("#full-screen-icon-close").addClass("invisible")
//       document.exitFullscreen();
//   }
   
// }
goFullScreen(){

  var elem = document.getElementById("camera_layout_wrap");
  $("#full-screen-icon-close").removeClass("invisible")
  $("#full-screen-icon-open").addClass("invisible")
  if(elem.requestFullscreen){
      elem.requestFullscreen();
  }
 
}
exitFullScreen(){
$("#full-screen-icon-open").removeClass("invisible")
$("#full-screen-icon-close").addClass("invisible")
if(document.exitFullscreen){
    document.exitFullscreen();
}


}



getinspection(){
  this.inspection_payload = {
    "part_name": this.partafterSelect,
    "inspection_id": this.running_inspection_id
  }
  this.marutiService.getInspection(this.inspection_payload).subscribe((data) => {
    //////console.log("yes")
  })
}


}
