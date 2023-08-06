# How to use this on local machine

---
1. Go to ds-backend-billing folder
    > This could be in ~/k8s-di-apps/ds-backend-billing

2. Run the commands 
    ```sh
    $ make clean
    
    $ make dev
    ```

---

## Minimal command required
```sh
$ ds-billing-app
```
## The above command looks for below files in the same directory mentioned in the first point above as default

ATB.xlsx

clearance.xlsx


## Note: If file names are different or present in the different directories, please use below command 
```sh
$ ds-billing-app \
    --atb '~/backend/OMD ATB 7-8-20.xlsx' \
    --clearance '~/backend/Omnicom Clearance report 07-17-20-1.xlsx'
```

## Default output file is below in same directory as folder in point 1 above
outputfile.xlsx

### or you can provide output file path parameter which will create output file at that path
```sh
$ ds-billing-app \
    --outputfile '~/customoutputfilename.xlsx'
```

## Full command 
```sh
$ ds-billing-app \
    --atb '~/backend/OMD ATB 7-8-20.xlsx' \
    --clearance '~/backend/Omnicom Clearance report 07-17-20-1.xlsx' \
    --outputfile '~/customoutputfilename.xlsx'
```