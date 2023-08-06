////////////////////////////////////////////////////////////////////////////////
// Copyright 2020 NAVER Corp
// 
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License.  You may obtain a copy
// of the License at
// 
//   http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
// License for the specific language governing permissions and limitations under
// the License.
////////////////////////////////////////////////////////////////////////////////
/*
 * SafeSharedState.cpp
 *
 *  Created on: Sep 16, 2020
 *      Author: eeliu
 */

#include "SafeSharedState.h"

namespace Cache {
bool SafeSharedState::checkTraceLimit(int64_t timestamp)
{
    time_t ts = (timestamp != -1) ?(timestamp) :(std::time(NULL));
    
    if(global_agent_info.trace_limit == -1)
    {
        return false;
    }

    if(global_agent_info.trace_limit == 0)
    {
        // block without any checking
        goto BLOCK;
    }

    if( this->_global_state->timestamp != ts )
    {
        this->_global_state->timestamp = ts;
        this->_global_state->tick = 0 ;
        __sync_synchronize();
    }
    else if(this->_global_state->tick >= global_agent_info.trace_limit)
    {
        goto BLOCK;
    }else if(this->isReady() == false){
        goto BLOCK;
    }else
    {
        __sync_add_and_fetch(&this->_global_state->tick,1);
    }
    return false;
BLOCK:
    pp_trace("This span dropped. max_trace_limit:%d current_tick:%d offLine:%d",global_agent_info.trace_limit,
        this->_global_state->tick,this->isReady()?(1):(0));
    return true;
}


SafeSharedState::SafeSharedState()
{
    this->_global_state = (SharedState*)fetch_shared_obj_addr();
}

} /* namespace Cache */
