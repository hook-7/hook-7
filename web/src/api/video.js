import service from "@/utils/request";



export async function getVideos(){
   const req = await service.get("/fileList");
    return req.data;
}