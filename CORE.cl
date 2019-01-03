__kernel void evr_cyc(__global const float *positions, 
                  __global const float *matrix, 
                  const float min_dis,
                  const float max_dis,
                  const int bin_num,
                  __global float *trans)
{
    //Calculate the structure model of the annular chromosome.
    int gid = get_global_id(0);

    float x = positions[gid * 3];
    float y = positions[gid * 3 + 1];
    float z = positions[gid * 3 + 2];

    float3 divec = (float3)(0.0, 0.0, 0.0);
    float3 ervec = (float3)(0.0, 0.0, 0.0);

    float mod = 0.0;
    float err = 0.0;
    float dis = 0.0;

    for(int i = 0; i < bin_num; i++){
        if(i == gid)
            continue;
        
        divec.x = positions[i * 3] - x;
        divec.y = positions[i * 3 + 1] - y;
        divec.z = positions[i * 3 + 2] - z;
        mod = sqrt(divec.x * divec.x + divec.y * divec.y + divec.z * divec.z);

        dis = matrix[i * bin_num + gid];
        if(dis == 0 || mod == 0)
            continue;

        divec /= mod;
        if(i == (gid + 1) % bin_num || i == (gid - 1) % bin_num)
        {
            if(mod > max_dis)
                err = mod - max_dis;
            else{
                if(mod < min_dis)
                    err = mod - min_dis;
                else
                    err = 0.0;
            }
        }
        else{
            err = mod - dis;
        }

        divec = divec * err;

        ervec += divec;
    }
    ervec /= bin_num;
    trans[gid * 3] = ervec.x;
    trans[gid * 3 + 1] = ervec.y;
    trans[gid * 3 + 2] = ervec.z;
}

__kernel void evr_lin(__global const float *positions, 
                  __global const float *matrix, 
                  const float min_dis,
                  const float max_dis,
                  const int bin_num,
                  __global float *trans)
{
    //Calculate the structure model of the annular chromosome.
    int gid = get_global_id(0);

    float x = positions[gid * 3];
    float y = positions[gid * 3 + 1];
    float z = positions[gid * 3 + 2];

    float3 divec = (float3)(0.0, 0.0, 0.0);
    float3 ervec = (float3)(0.0, 0.0, 0.0);

    float mod = 0.0;
    float err = 0.0;
    float dis = 0.0;

    for(int i = 0; i < bin_num; i++){
        if(i == gid)
            continue;
        
        divec.x = positions[i * 3] - x;
        divec.y = positions[i * 3 + 1] - y;
        divec.z = positions[i * 3 + 2] - z;
        mod = sqrt(divec.x * divec.x + divec.y * divec.y + divec.z * divec.z);

        dis = matrix[i * bin_num + gid];
        if(dis == 0 || mod == 0)
            continue;

        divec /= mod;
        if(i == gid + 1 || i == gid - 1)
        {
            if(mod > max_dis)
                err = mod - max_dis;
            else{
                if(mod < min_dis)
                    err = mod - min_dis;
                else
                    err = 0.0;
            }
        }
        else{
            err = mod - dis;
        }

        divec = divec * err;

        ervec += divec;
    }
    ervec /= bin_num;
    trans[gid * 3] = ervec.x;
    trans[gid * 3 + 1] = ervec.y;
    trans[gid * 3 + 2] = ervec.z;
}
