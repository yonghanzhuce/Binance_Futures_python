// 创建Uniswap的交易合约
pragma solidity ^0.5.0;

import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";
import "github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol";

contract Uniswap {
    using SafeMath for uint256;
    // 交易对
    struct Pair {
        // 交易对的token地址
        address tokenA;
        address tokenB;
        // tokenA和tokenB的比例
        uint256 ratio;
    }
    // 交易对的数组
    Pair[] pairs;
    // 交易对的映射
    mapping(address => mapping(address => uint256)) pairFor;

    // 添加交易对
    function addPair(address tokenA, address tokenB, uint256 ratio) public {
        // 创建交易对
        Pair memory pair = Pair(tokenA, tokenB, ratio);
        // 添加到交易对数组中
        pairs.push(pair);
        // 添加到交易对映射中
        pairFor[tokenA][tokenB] = pairs.length - 1;
    }

    // 获取交易对的数量
    function getPairCount() public view returns (uint256) {
        return pairs.length;
    }

    // 交易
    function swap(address tokenA, address tokenB, uint256 amount) public {
        // 获取交易对的索引
        uint256 pairIndex = pairFor[tokenA][tokenB];
        // 获取交易对
        Pair memory pair = pairs[pairIndex];
        // 获取tokenA的数量
        uint256 amountA = IERC20(tokenA).balanceOf(address(this));
        // 获取tokenB的数量
        uint256 amountB = IERC20(tokenB).balanceOf(address(this));
        // 计算tokenA的数量
        uint256 amountATo = amount.mul(amountA).div(amountA.add(amountB));
        // 计算tokenB的数量
        uint256 amountBTo = amount.mul(amountB).div(amountA.add(amountB));
        // 转移tokenA
        IERC20(tokenA).transfer(msg.sender, amountATo);
        // 转移tokenB
        IERC20(tokenB).transfer(msg.sender, amountBTo);
    }
}


