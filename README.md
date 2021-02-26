# venom
第一次提交，测试连接
/**
 * 
 */
package com.huixin.cdp.service.impl;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import javax.annotation.Resource;
import cn.hutool.crypto.Mode;
import cn.hutool.crypto.Padding;
import cn.hutool.crypto.symmetric.AES;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.IdWorker;
import com.huixin.cdp.CreditResult;
import com.huixin.cdp.entity.*;
import com.huixin.cdp.entity.Company;
import com.huixin.cdp.entity.Credit;
import com.huixin.cdp.entity.Source;
import com.huixin.cdp.entity.System;
import com.huixin.cdp.enums.*;
import com.huixin.cdp.manager.DBManager;
import com.huixin.cdp.manager.DoRouteService;
import com.huixin.cdp.manager.ratelimiter.RateUtils;
import com.huixin.cdp.mapper.*;
import com.huixin.cdp.service.CreditTableService;
import com.huixin.cdp.util.ThreadPoolUtil;
import com.huixin.cdp.mapper.CompanyMapper;
import com.huixin.cdp.mapper.CreditMapper;
import com.huixin.cdp.mapper.SourceMapper;
import com.huixin.cdp.mapper.SystemMapper;
import com.huixin.cdp.sysAut.jwt.JwtTokenUtil;
import com.huixin.cdp.util.ShiroUtil;
import com.huixin.framework.base.exception.ServiceException;
import com.huixin.framework.web.dto.CommonResult;
import org.apache.commons.lang3.StringUtils;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.stereotype.Service;
import com.huixin.cdp.common.CreditResponse;
import com.huixin.cdp.common.ErrorCode;
import com.huixin.cdp.manager.CreditManager;
import com.huixin.cdp.service.CreditDataService;
import lombok.extern.slf4j.Slf4j;

/**资信统一入口类
 * 提供资信的同步异步接口
 * @author b00342
 *
 */

@Slf4j
@Service("creditDataService")
public class CreditDataServiceImpl implements CreditDataService {
	
	@Resource
	private CreditManager creditManager;
	
    @Resource
    private RedissonClient redissonClient;

    @Resource
	private RouteMapper routeMapper;

	@Resource
	private SourceMapper sourceMapper;

	@Resource
	private CreditMapper creditMapper;

	@Resource
	private DBManager dbManager;

	@Resource
	private CompanyMapper companyMapper;

	@Resource
	private DoRouteService doRouteService;

	@Resource
	private SystemMapper systemMapper;

	@Resource
	private JwtTokenUtil jwtTokenUtil;



	private static final AES aes = new AES(Mode.CBC, Padding.ZeroPadding, "1111222233337777".getBytes(),"1111222233337777".getBytes());



	@Override
	public CreditResponse getCreditData(List<String> sourceIdList,String systemCode, String creditCode, String companyCode, String custNo, String inputJson,String teamCode) {
		CreditResponse creditResponse = new CreditResponse();
		List<Route> routeList = routeMapper.selectList(new QueryWrapper<Route>().lambda().in(Route::getSourceId,sourceIdList));

		List<Source> sourceList=new ArrayList<>();


		if(sourceIdList.size()>1){
			//若为优先模式，则将可用数据源列表根据优先级排序
			if(RouteType.LEVEL.equals(routeList.get(0).getRouteType())){
				routeList=routeList.stream().sorted(Comparator.comparing(Route::getPriority)).collect(Collectors.toList());
				sourceList=sourceMapper.selectBatchIds(routeList.stream().map(Route::getSourceId).collect(Collectors.toList()));
			}else {
				sourceList=sourceMapper.selectBatchIds(sourceIdList);
			}
		}else {
			//若可用数据源数量为1，则不需要路由
			Source source = sourceMapper.selectById(sourceIdList.get(0));
			if(null==source){
				creditResponse.setErrorCode(ErrorCode.NO_AVAILABLE_SOURCE.getCode());
				creditResponse.setErrorMessage(ErrorCode.NO_AVAILABLE_SOURCE.getMsg());
				creditResponse.setSuccess(false);
				return creditResponse;
			}
			sourceList.add(source);
		}

		//将source和其路由参数放在map中
		int len=sourceList.size();

		HashMap<Source,Route> sourceRouteMap=new HashMap<>(len);
		for (int i = 0; i < len; i++) {
				sourceRouteMap.put(sourceList.get(i), routeList.get(i));
		}
		//根据可用数据源的list判断是否需要路由
		//当有多个可用数据源时，执行路由方法，筛选出数据源，并判断是否限流
//		Source source=null;
//		try {
//			source = checkRateAndRoute(sourceRouteMap, creditCode, companyCode, systemCode);
//		}catch (ServiceException e){
//			log.error("执行限流路由流程出错: {} 错误类型{}",e.getRespCode().getMsg(),e.getMsg());
//			creditResponse.setErrorCode(e.getRespCode().getCode());
//			creditResponse.setErrorMessage(e.getRespCode().getMsg());
//			creditResponse.setSuccess(false);
//			return creditResponse;
//		}

		try {
			String key = new StringBuilder("cdp_").append(creditCode).append("_").append(companyCode).append("_").append(custNo).toString();
			RLock lock = redissonClient.getLock(key);
			boolean lockResult = false;
			
			try {
				lockResult = lock.tryLock(1, 30, TimeUnit.SECONDS);
				if(!lockResult) {
					creditResponse.setErrorCode(ErrorCode.DUPLICATE_REQUEST.getCode());
					creditResponse.setErrorMessage(ErrorCode.DUPLICATE_REQUEST.getMsg());
					creditResponse.setSuccess(false);
					return creditResponse;
				}
				creditResponse = creditManager.getCreditData(sourceRouteMap,systemCode,creditCode,companyCode,custNo, inputJson,teamCode);
			} catch(Exception e) {
				log.error("getCreditData error : datasource:{}  dataCompany:{} custNo: {}",creditCode,companyCode,custNo, e);
			} finally {
				if(lockResult) {
					lock.unlock();
				}
			}
		} catch (Exception e) {
			log.error("getCreditData error : datasource:{}  dataCompany:{} custNo: {}",creditCode,companyCode,custNo, e);
			creditResponse.setErrorCode(ErrorCode.SERVICE_ERROR.getCode());
			creditResponse.setErrorMessage(ErrorCode.SERVICE_ERROR.getMsg());
			creditResponse.setSuccess(false);			
		}
		
		return creditResponse;
	}



	@Override
	public CreditResponse getCreditDataByRequestId(String requestId,String creditCode) {
		CreditResponse creditResponse=new CreditResponse();

		if(StringUtils.isBlank(requestId)||StringUtils.isBlank(creditCode)){
			creditResponse.setErrorCode(ErrorCode.PARAM_VALIDATE_FAIL.getCode());
			creditResponse.setErrorMessage(ErrorCode.PARAM_VALIDATE_FAIL.getMsg());
			creditResponse.setSuccess(false);
			return creditResponse;
		}

		Credit credit = creditMapper.selectOne(new QueryWrapper<Credit>().eq("code", creditCode));
		if(null==credit){
			creditResponse.setErrorCode(ErrorCode.PARAM_VALIDATE_FAIL.getCode());
			creditResponse.setErrorMessage(ErrorCode.PARAM_VALIDATE_FAIL.getMsg());
			creditResponse.setSuccess(false);
			return creditResponse;
		}

		CreditTableService creditTableService = dbManager.buildCreditTableServiceByCreditCode(creditCode);
		CreditResult creditResult = creditTableService.queryCreditResultByAsyncRequestId(credit.getResultTable(), requestId);

		if(null==creditResult){
			creditResponse.setSuccess(false);
			creditResponse.setErrorCode(ErrorCode.SERVICE_ERROR.getCode());
			creditResponse.setErrorMessage(ErrorCode.SERVICE_ERROR.getMsg());

			return creditResponse;
		}
		creditResponse.setSuccess(true);
		creditResponse.setCreditResult(creditResult);

        return creditResponse;
	}


	@Override
	public String getCreditDataAsync(List<String> sourceIdList,String systemCode, String bizType, String dataChannel, String custNo,String inputJson,String teamCode) {
		String requestId= IdWorker.getIdStr();
		ThreadPoolExecutor pool = ThreadPoolUtil.getPool();


		pool.execute(() -> {

			CreditResponse response = getCreditData(sourceIdList,systemCode,bizType,dataChannel,custNo,inputJson,teamCode);
				CreditResult creditResult = response.getCreditResult();
				if(null!=creditResult){
					CreditTableService creditTableService = dbManager.buildCreditTableServiceByCreditCode(bizType);
					creditTableService.updateCreditResult(creditResult,"async_request_id",requestId);
				}
		});

		return requestId;
	}

	@Override
	public CommonResult applyToken(String userKey, String userPassword) {
		log.info("POST请求登录");
		String password=null;
		try {
			password = decrypt(userPassword);
		}catch (Exception e){
			return CommonResult.failed("密码加密不正确");
		}

		if (StringUtils.isBlank(userKey)) {
			return CommonResult.failed("系统Code不能为空");
		}
		if (StringUtils.isBlank(password)) {
			return CommonResult.failed("密码不能为空");
		}

		System system = systemMapper.selectOne(new QueryWrapper<System>().lambda().eq(System::getSystemCode,userKey));


		if (system == null) {
			return CommonResult.failed("账号不存在");
		}
		if (!system.getPassword().equals(ShiroUtil.md5(password))) {
			return CommonResult.failed("密码不正确");
		}
		if (!system.getEnable()) {
			return CommonResult.failed("账号被禁用");
		}

		String token=jwtTokenUtil.generateToken(system);
		//shiroRedisCacheManager.getCache("alive_token").put(username,token);
		ConcurrentMap<String, Object> concurrentMap=new ConcurrentHashMap<>();
		concurrentMap.put("token",token);
		log.info(" 上游系统:  " + system.getSystemName() + ",获取token成功！ ");
		return CommonResult.success(concurrentMap);
	}

	/**
	 * 解密
	 * @param encrypt
	 * @return
	 */
	private String decrypt(String encrypt) {
		/** AES加解密 */
		String s= aes.decryptStr(encrypt).replace("\"", "");
		return s;
	}


//	/**
//	 * 检查数据源限流和路由功能
//	 * @param sourceRouteMap 可用数据源及其路由参数的map
//	 * @param creditCode 资信code
//	 * @param systemCode 上游系统code
//	 * @return 未被限流且路由后的数据源
//	 */
//	public Source checkRateAndRoute(HashMap<Source,Route> sourceRouteMap,String creditCode ,String systemCode){
//		Source source=null;
//		boolean rateSuccess=false;
//		while (true){
//			if(sourceRouteMap.size()>1){
//				source=doRouteService.getCredit1( sourceRouteMap,creditCode);
//				//如果source为null说明该资信项所有数据源都未配置路由参数
//				if(null==source){
//					throw new ServiceException(ErrorCode.ROUTE_FAILED);
//				}
//
//				String companyCode=companyMapper.selectOne(new QueryWrapper<Company>().eq("id",source.getDataCompanyId())).getCode();
//				//校验限流
//
//				rateSuccess = RateUtils.tryAcquire(source.getCode(), companyCode, systemCode);
//
//				//如果检验通过，直接跳出循环
//				if(rateSuccess){
//					break;
//				}else {
//					//检验不通过，把当前数据源从可用数据源列表中移除，并重新进入循环
//					sourceRouteMap.remove(source);
//					log.info("数据源:{} 被限流，路由下一个可用数据源",source.getCode());
//					continue;
//				}
//			}else {
//				//当只剩一个可用数据源时
//				List<Source> sourceList = (List<Source>) sourceRouteMap.keySet();
//				source = sourceList.get(0);
//				String companyCode=companyMapper.selectOne(new QueryWrapper<Company>().eq("id",source.getDataCompanyId())).getCode();
//				//校验限流
//				rateSuccess = RateUtils.tryAcquire(source.getCode(), companyCode, systemCode);
//				//如果检验通过，直接跳出循环
//				if(rateSuccess){
//					break;
//				}else {
//					log.info("数据源:{}被限流，无数据源可用，返回查询结果",source.getCode());
//					//检验不通过，说明可用数据源都被限流，直接返回错误
//					throw new ServiceException(ErrorCode.RATE_LIMIT);
//				}
//			}
//		}
//		if(null==source){
//			throw new ServiceException(ErrorCode.SERVICE_ERROR);
//		}
//
//		return source;
//	}
}









package com.huixin.cdp.aop;

import com.huixin.cdp.mapper.ExceptionMonitorMapper;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.exception.ExceptionUtils;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;

/**
 * @author h00929
 * @version 1.0
 * @description do it
 * @date 2021/2/26 14:04
 */
@Aspect
@Component
@Slf4j
public class ExceptionMonitorAop {

    @Resource
    ExceptionMonitorMapper exceptionMonitorMapper;

    @Pointcut(value = "execution(* com.huixin.cdp.service.impl.CreditDataServiceImpl.*(..))")
    private void pointCut() {//定义一个切入点 后面的通知直接引入切入点方法pointCut即可
    }

    @Before(value = "pointCut()")
    public void doBefore(JoinPoint joinPoint) {

    }

    @AfterThrowing(throwing = "throwable", pointcut = "pointCut()")
    public void doAfter(JoinPoint joinPoint, Throwable throwable) {
        String message = ExceptionUtils.getMessage(throwable);
        log.error(message);

        // 所属类名
        String className = joinPoint.getTarget().getClass().getName();
        // 方法名
        String methodName = joinPoint.getSignature().getName();
        // 目标方法传入的参数
        Object[] params = joinPoint.getArgs();


    }


}







