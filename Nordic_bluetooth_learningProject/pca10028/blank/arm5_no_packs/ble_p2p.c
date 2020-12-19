#include <stdint.h>
#include "nrf.h"

//                                
static uint8_t p2p_adv_data_slave[10] = {0x00,0x06,0x00,0x9A,0x78,0x56,0x34,0x12,0xaf,0xff};

void timer_setup_p2p();
void gpiote_setup_p2p(void);
void ppi_setup_p2p(void);
void init_input_pins(void);

void ble_radio_setup_p2p(){
  init_input_pins();
	ppi_setup_p2p();
	gpiote_setup_p2p();
	timer_setup_p2p();

  NRF_RADIO->PACKETPTR = (uint32_t) &(p2p_adv_data_slave[0]);
}



void timer_setup_p2p(void)
{
	
	/*Causes: Clear and stop timer on compare match */
	NRF_TIMER0->SHORTS = ((TIMER_SHORTS_COMPARE0_CLEAR_Enabled << TIMER_SHORTS_COMPARE0_CLEAR_Pos) & TIMER_SHORTS_COMPARE0_CLEAR_Msk)
											|((TIMER_SHORTS_COMPARE0_STOP_Enabled << TIMER_SHORTS_COMPARE0_STOP_Pos) & TIMER_SHORTS_COMPARE0_STOP_Msk);
	
	NRF_TIMER0->BITMODE = TIMER_BITMODE_BITMODE_32Bit;



	NRF_TIMER0->PRESCALER = 8; 
	NRF_TIMER0->CC[0] = 32000;
}


void gpiote_setup_p2p(void) // Configures Tasks and events for GPIO
{
	// There are max 4 GPIO Tasks/Events (Shared between them)
    // Tasks are implicitly set as outpusts, while events are set as inputs

    // Event on pin 1 (Serve "Master")
	NRF_GPIOTE->CONFIG[0] = ((GPIOTE_CONFIG_MODE_Event << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)                                        // Configure as event                                 
													|	((1UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)                                 // PIN 1 
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk) // The event is when the pinis toggled                               
													| ((GPIOTE_CONFIG_OUTINIT_Low << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);      // Set initial value for the pin                          

    // Event on button 1 
	NRF_GPIOTE->CONFIG[1] = ((GPIOTE_CONFIG_MODE_Event << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)                                                                
													|	((17UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)                                                        
													| ((GPIOTE_CONFIG_POLARITY_HiToLo << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)                         
													| ((GPIOTE_CONFIG_OUTINIT_High << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);                
	// Toggle-led2-task	("Heartbeat")
	NRF_GPIOTE->CONFIG[2] = ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)                                         // Configure as task 
													|	((22UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)                                // PIN 22 
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk) // Toggle pin when task is called
													| ((GPIOTE_CONFIG_OUTINIT_Low << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);      // Set initial value to low
	// Toggle pin 2 ( Drive "Slave")
	NRF_GPIOTE->CONFIG[3] = ((GPIOTE_CONFIG_MODE_Task << GPIOTE_CONFIG_MODE_Pos) & GPIOTE_CONFIG_MODE_Msk)
													|	((2UL << GPIOTE_CONFIG_PSEL_Pos) & GPIOTE_CONFIG_PSEL_Msk)
													| ((GPIOTE_CONFIG_POLARITY_Toggle << GPIOTE_CONFIG_POLARITY_Pos) & GPIOTE_CONFIG_POLARITY_Msk)
													| ((GPIOTE_CONFIG_OUTINIT_High << GPIOTE_CONFIG_OUTINIT_Pos) & GPIOTE_CONFIG_OUTINIT_Msk);
													
}


void ppi_setup_p2p(void) 
{
	/*
	CH0: Master Drive -> TIMER_START
	CH1: TIMER_CC -> RADIO_START
	CH2: RADIO_END -> TOGGLE_LED
	CH3: BUTTON4_PRESSED -> RADIO_START  For debug 
	*/
	
	NRF_PPI->CHENSET |=       ((PPI_CHENSET_CH0_Enabled << PPI_CHENSET_CH0_Pos) & PPI_CHENSET_CH0_Msk)
							| ((PPI_CHENSET_CH1_Enabled << PPI_CHENSET_CH1_Pos) & PPI_CHENSET_CH1_Msk)
							| ((PPI_CHENSET_CH2_Enabled << PPI_CHENSET_CH2_Pos) & PPI_CHENSET_CH2_Msk)
							| ((PPI_CHENSET_CH3_Enabled << PPI_CHENSET_CH3_Pos) & PPI_CHENSET_CH3_Msk)
                            | ((PPI_CHENSET_CH4_Enabled << PPI_CHENSET_CH4_Pos) & PPI_CHENSET_CH4_Msk);
   
   
   
   
    //                       "Slave"-role
    // Toggle PIN1 ==> countdown to serve master
	NRF_PPI->CH[0].EEP = (uint32_t) &(NRF_GPIOTE->EVENTS_IN[0]);
	NRF_PPI->CH[0].TEP = (uint32_t) &(NRF_TIMER0->TASKS_START);
	
    // Send BLE-message after timeout
	NRF_PPI->CH[1].EEP = (uint32_t) &(NRF_TIMER0->EVENTS_COMPARE);
	NRF_PPI->CH[1].TEP = (uint32_t) &(NRF_RADIO ->TASKS_START   );




    
    //                        "Master"- role 
    // Drive slave when button 1 is pressed
    NRF_PPI->CH[2].EEP =  (uint32_t) &(NRF_GPIOTE->EVENTS_IN[1]);
    NRF_PPI->CH[2].TEP =  (uint32_t) &(NRF_GPIOTE->TASKS_OUT[3]);

    // Transmit BLE-message when button 1 is pressed
    NRF_PPI->CH[3].EEP = (uint32_t) &(NRF_GPIOTE->EVENTS_IN[1]);
    NRF_PPI->CH[3].TEP = (uint32_t) &(NRF_RADIO->TASKS_START  );




    //                      Both master and slave
    
    // Heartbeat
	NRF_PPI->CH[4].EEP = (uint32_t) &(NRF_RADIO->EVENTS_END);
	NRF_PPI->CH[4].TEP = (uint32_t) &(NRF_GPIOTE->TASKS_OUT[2]);
}


void init_input_pins(void)
{
        // button 1
		NRF_GPIO->PIN_CNF[17] = ((GPIO_PIN_CNF_DIR_Input << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)                          // Set pin 17 as input (Might be redundant)
												|	((GPIO_PIN_CNF_PULL_Pullup << GPIO_PIN_CNF_PULL_Pos) & GPIO_PIN_CNF_PULL_Msk)  // Enable pill-up
												|	((GPIO_PIN_CNF_SENSE_Low << GPIO_PIN_CNF_SENSE_Pos) & GPIO_PIN_CNF_SENSE_Msk); // Sense low ???
    // pin 1 ("Slave" input)
        NRF_GPIO->PIN_CNF[1] = ((GPIO_PIN_CNF_DIR_Input << GPIO_PIN_CNF_DIR_Pos) & GPIO_PIN_CNF_DIR_Msk)
										|	((GPIO_PIN_CNF_PULL_Pullup << GPIO_PIN_CNF_PULL_Pos) & GPIO_PIN_CNF_PULL_Msk)
										|	((GPIO_PIN_CNF_SENSE_Low << GPIO_PIN_CNF_SENSE_Pos) & GPIO_PIN_CNF_SENSE_Msk);    
}



